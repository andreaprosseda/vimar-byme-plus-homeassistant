import json

from .file import read_file


def read_json(file_name: str) -> dict:
    content = read_file(file_name)
    return json.loads(content)


def json_dumps(value: str) -> str:
    json_value = json.dumps(value)
    # return remove_nulls(json_value)
    return json_value


def remove_nulls(value):
    if isinstance(value, dict):
        return {k: remove_nulls(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [remove_nulls(item) for item in value if item is not None]
    return value
