import logging


def get_logger(name, log_level="INFO"):
    """Factory function for obtaining logging object

    :Returns: logging.Logger

    :param name: The name for the log object
    :type name: String

    :param verbose: Set to True for debug logging. Default is False.
    :type verbose: Boolean
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(filename)s]: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def resolve_path(path, base):
    """
    Generate an absolute path from a provided path and base.

    :param path: The filesystem path to resolve.
    :param base: Enables resolution for relative paths.
    """
    p = path
    if not path.anchor == "/":
        p = base / path
    return p.resolve()


def path_is_valid(resolved_path, root_path):
    """
    The path tested is a member of a provided hierarchy.

    :param resolved_path: The absolute path to test.
    :param root_path: The top level directory the tested path must be a member of.
    """
    return resolved_path.is_relative_to(root_path)
