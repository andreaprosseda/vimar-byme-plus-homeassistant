import os

from ..config.const import DATA_PATH


def file_exists(file_name: str) -> bool:
    file_path = get_file_path(file_name)
    return os.path.isfile(file_path)


def read_file(file_name: str) -> str:
    file_path = get_file_path(file_name)
    with open(file_path) as file:
        content = file.read()
    return content


def save_file(content: str, file_name: str) -> None:
    file_path = get_file_path(file_name)
    with open(file_path, "w") as file:
        file.write(content)


def remove_file(file_name: str) -> None:
    if not file_name:
        return
    if file_exists(file_name):
        file_path = get_file_path(file_name)
        os.remove(file_path)


def create_data_if_not_exists() -> str:
    os.makedirs(_get_data_path(), exist_ok=True)


def get_file_path(file_name: str) -> str:
    create_data_if_not_exists()
    return get_data_path() + file_name


def get_db_name() -> str:
    path = get_data_path()
    for file_name in os.listdir(path):
        if file_name.endswith(".db"):
            return file_name
    return None


def get_data_path() -> str:
    return _get_data_path() + "/"


def _get_data_path() -> str:
    if "standalone" in __name__:
        return "standalone/data"
    return DATA_PATH
