import logging
from .file import get_file_path, remove_file

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if "standalone" in __name__:
    level = logging.DEBUG
    logger.setLevel(level)
    
    remove_file("app.log")
    file_handler = logging.FileHandler(get_file_path("app.log"), mode="a")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def log_info(__name__: str, message: str):
    logger.name = __name__
    logger.info(message)


def log_debug(__name__: str, message: str):
    logger.name = __name__
    logger.debug(message)


def log_error(__name__: str, message: str):
    logger.name = __name__
    logger.error(message)
