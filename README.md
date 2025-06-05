# Sawmill API

## Local dev setup

### Prerequisites
To get started, you'll need Python3, Docker or Podman, the PostgreSQL header files installed (`libpq-dev` for Debian/Ubuntu, `postgresql-libs` for RHEL) and `make`.

It's also **highly** recommened that you setup a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html), but hey, it's your system.

### Run

1. `make bootstrap`
2. `make images`
3. `make up`
 *  To initialize the database, run: `docker compose exec -it oltp-1 ./cockroach --host=oltp-1:26357 init --insecure`

You can now access the API via `https://localhost:8000`.


# License Information
This project is licensed under the Business Source License 1.1. It's free for personal or internal use.
Commercial use (including SaaS, resale, or bundling in hardware) requires a commercial license.
The license will convert to Apache 2.0 on June 1, 2030.

Long story short, anyone can use it at their home or at work for free.
If you want to try and profit off it directly, you'll need a license.
