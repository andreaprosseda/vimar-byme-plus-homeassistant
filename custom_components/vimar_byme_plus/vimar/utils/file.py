import os
from ..config.const import DATA_PATH

def file_exists(file_name: str) -> bool:
    file_path = get_file_path(file_name)
    return os.path.isfile(file_path)


def read_file(file_name: str) -> str:
    file_path = get_file_path(file_name)
    with open(file_path, "r") as file:
        content = file.read()
    return content


def save_file(content: str, file_name: str) -> None:
    file_path = get_file_path(file_name)
    with open(file_path, "w") as file:
        file.write(content)


def remove_file(file_name: str) -> None:
    if file_exists(file_name):
        file_path = get_file_path(file_name)
        os.remove(file_path)


def get_file_path(file_name: str) -> str:
    return get_data_path() + file_name


def get_data_path() -> str:
    return DATA_PATH
