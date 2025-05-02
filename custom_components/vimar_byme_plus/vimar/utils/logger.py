import logging

from ..model.repository.user_component import UserComponent
from .file import get_file_path, remove_file

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
level = logging.DEBUG

if "standalone" in __name__:
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


def log_info(module_name: str, message: str):
    result = f"[{module_name}] {message}"
    logger.info(result)


def log_debug(module_name: str, message: str):
    result = f"[{module_name}] {message}"
    logger.debug(result)


def log_error(module_name: str, message: str):
    result = f"[{module_name}] {message}"
    logger.error(result)


def not_implemented(module_name: str, component: UserComponent):
    name = component.name
    sstype = component.sstype
    message = f"[{name}] Component of type {sstype} not yet implemented!"
    log_error(module_name, message)
