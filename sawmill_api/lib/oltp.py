"""
Interact with an Online Transaction Processing (OLTP) database.
"""

import time
from collections import deque
from contextlib import contextmanager
from threading import Semaphore
from functools import wraps
from textwrap import dedent
import pathlib
import socket

from sawmill_api import settings

import psycopg2
from psycopg2.extensions import register_adapter, QuotedString

ENGINE = None


register_adapter(pathlib.Path, lambda p: QuotedString(str(p)))


class BlockingConnectionPool:
    """
    A thread safe way to manage database connections.
    """

    def __init__(self, host, port, user, password, dbname, max_connections=10):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._dbname = dbname
        self._max_connections = max_connections
        self._pool = deque(
            (None for _ in range(max_connections)), maxlen=max_connections
        )
        self.semaphore = Semaphore(max_connections)

    def init_app(self, app):
        global ENGINE
        if ENGINE is None:
            ENGINE = self

    @contextmanager
    def get_conn(self, timeout=None, retries=5):
        if self.semaphore.acquire(timeout=timeout):
            raise TimeoutError(
                f"Unable to obtain a database connection after {timeout} seconds."
            )
        conn = self._pool.pop()
        if conn is None:
            for attempt in range(1, retries):
                try:
                    conn = psycopg2.connect(
                        host=self._host,
                        port=self._port,
                        dbname=self._dbname,
                        user=self._user,
                        password=self._password,
                    )
                except Exception:
                    time.sleep(attempt)
                else:
                    break
            if attempt == retries - 1:
                conn = psycopg2.connect(
                    host=self._host,
                    port=self._port,
                    dbname=self._dbname,
                    user=self._user,
                    password=self._password,
                )
        try:
            yield conn
        except psycopg2.OperationalError as doh:
            cause = doh.__cause__ or doh.__context__
            if isinstance(
                cause,
                (
                    socket.timeout,
                    socket.gaierror,
                    ConnectionResetError,
                    ConnectionAbortedError,
                ),
            ):
                conn = None
            else:
                raise
        finally:
            self._pool.append(conn)
            self.semaphore.release()

    def close(self):
        for conn in self._pool:
            if conn:
                conn.close()


def with_cursor(timeout=None):
    """
    A handy way to save a pile of indent space and boiler plate to get a cursor.

    Decorated functions will have `cursor` passed in as the first
    argument.
    """

    def real_decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if ENGINE is None:
                error = "Must create a database object and run `init_app` before using `with_cursor`."
                raise RuntimeError(error)
            with ENGINE.get_conn(timeout=timeout) as conn:
                with conn.cursor() as cursor:
                    try:
                        result = func(cursor, *args, **kwargs)
                    except psycopg2.Error as doh:
                        conn.rollback()
                        raise doh from None
                    else:
                        conn.commit()
                        return result

        return inner

    return real_decorator


def rows_to_dicts(cursor):
    """
    Turn row tuples into normal Python dictionaries.

    The options in `psycopg2.extras` are antiquated; vanilla Python
    dictionaries have come a *long* way starting with Python 3.6.
    """
    column_names = [c.name for c in cursor.description]
    rows = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return rows


@with_cursor()
def example(cursor):
    """
    A placeholder example while I work on real ones ;)
    """
    sql = dedent(
        """
        SELECT relname
        FROM pg_class
        WHERE relkind='r'
            AND relname !~ '^(pg_|sql_)'
        """
    )
    cursor.execute(sql)
    return rows_to_dicts(cursor)


@with_cursor()
def get_api_settings(cursor) -> dict[str, list]:
    """
    Obtain the settings used by the API.
    """
    sql = dedent(
        """\
        SELECT
            section,
            name,
            value
        FROM api.settings
        """
    )
    cursor.execute(sql)
    grouped_by_section = {}
    for row in cursor.fetchall():
        section, name, value = row
        section_group = grouped_by_section.setdefault(section, {})
        section_group[name] = value
    return grouped_by_section


@with_cursor()
def set_api_setting(cursor, setting: settings.Section):
    """
    Save the current section settings ot the database.
    """
    sql = dedent(
        """\
        INSERT INTO api.settings (section, name, value)
        VALUES (%s, %s, %s)
        ON CONFLICT (section, name)
        DO UPDATE
        SET
            value = excluded.value
        WHERE
            api.settings.value IS DISTINCT FROM excluded.value
        ;
        """
    )
    params = [
        (
            settings.title_to_dash(setting.__class__.__name__),
            name,
            value,
        )
        for name, value in iter(setting)
    ]
    cursor.executemany(sql, params)
