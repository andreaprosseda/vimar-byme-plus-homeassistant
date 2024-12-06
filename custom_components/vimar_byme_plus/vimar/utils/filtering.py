def flat(nested_list: list[list]) -> list:
    return [value for sublist in nested_list for value in sublist]


def filter_none(values: list) -> list:
    result = []
    for value in values:
        if value:
            result.append(value)
    return result
