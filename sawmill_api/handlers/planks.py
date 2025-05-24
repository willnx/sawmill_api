import subprocess
import pathlib
import zlib
import pydantic
from flask import Blueprint, request, Response

from sawmill_api import utils
from sawmill_api.lib.smsh.parser import parse


planks_api = Blueprint("planks_api", __name__, url_prefix="/api/1/planks")

# TODO: Make configurable once settings are "a thing"
CHUNK_READ_SIZE = 8192
LOG_ROOT = pathlib.Path("/var/log")

log = utils.get_logger(__name__)


class PlankRequest(pydantic.BaseModel):
    cwd: str
    command: str = "cat"


@planks_api.route("/", methods=["GET"])
def get_planks():
    """Slice & dice logs for analysis."""
    command = request.args.get("command")
    cwd = request.args.get("cwd")
    if not (cwd and command):
        return "Missing required params", 400
    current_working_directory = utils.resolve_path(pathlib.Path(cwd), LOG_ROOT)
    if not utils.path_is_valid(current_working_directory, LOG_ROOT):
        return f"Provided CWD {current_working_directory} is not under {LOG_ROOT}", 400

    commands, error = parse(command, current_working_directory, LOG_ROOT)
    if error:
        return error, 400
    log.info(f"FINDME: {commands}")

    headers = {
        "Transfer-Encoding": "chunked",
        "Content-Type": "text/plain; charset=utf-8",
    }
    for encoding in request.headers.get("Accept-Encoding", "").split(","):
        if encoding.lower().strip() == "gzip":
            headers["Content-Encoding"] = "gzip"
            chunker = compressed_chunk_encoding
            break
    else:
        chunker = chunk_transfered_encoding
    stream = pipeline(commands, current_working_directory)
    return Response(chunker(stream), headers=headers)


def chunk_transfered_encoding(stream):
    """Stream the data in chunks via plain text."""
    while True:
        chunk = stream.read(CHUNK_READ_SIZE)
        if chunk:
            yield chunk.decode("utf-8")
        else:
            break


def compressed_chunk_encoding(stream):
    """
    For clients that support gzip compression.
    """
    compressor = zlib.compressobj(
        level=6,
        method=zlib.DEFLATED,
        wbits=16 + zlib.MAX_WBITS,  # gzip format
        memLevel=8,
        strategy=zlib.Z_DEFAULT_STRATEGY,
    )

    while True:
        chunk = stream.read(CHUNK_READ_SIZE)
        if not chunk:
            break

        compressed_chunk = compressor.compress(chunk)
        if compressed_chunk:
            yield compressed_chunk

    final_chunk = compressor.flush(zlib.Z_FINISH)
    if final_chunk:
        yield final_chunk


def pipeline(commands, current_working_directory):
    """Mimic the UNIX pipeline"""
    iterator = iter(commands)
    proc = subprocess.Popen(
        next(iterator),
        cwd=current_working_directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    for command in iterator:
        next_proc = subprocess.Popen(
            command,
            cwd=current_working_directory,
            stdin=proc.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        proc.stdout.close()  # Allow previous process to receive SIGPIPE
        proc = next_proc

    return proc.stdout
