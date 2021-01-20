def compare_convert_value(search, example):
    if isinstance(example, list):
        example = example[0]

    if len(search) == 1:
        search = search[0]

        if isinstance(example, int):
            return int(search)
        elif isinstance(example, float):
            return float(search)
        elif isinstance(example, bool):
            return bool(search)
    else:
        # The search value is a list
        if isinstance(example, int):
            return [int(item) for item in search]
        elif isinstance(example, float):
            return [float(item) for item in search]
        elif isinstance(example, bool):
            return [bool(item) for item in search]

    return search


def compare_basis(test_value_orig, comparison, value):
    test_value = test_value_orig
    if isinstance(test_value_orig, list) and not isinstance(value, list) and len(test_value_orig) == 1:
        test_value = test_value_orig[0]

    if comparison == "==":
        return test_value == value
    elif comparison == ">=":
        return test_value >= value
    elif comparison == ">":
        return test_value > value
    elif comparison == "<=":
        return test_value <= value
    elif comparison == "<":
        return test_value < value
    elif comparison == "!=":
        return test_value != value
    elif comparison == "in":
        return value in test_value_orig
    elif comparison == "in_list":
        return test_value_orig in value
    return False


def get_param_bool(param):
    return param != "0"


def get_param_int(param, alternative):
    try:
        val = int(param)
    except:
        val = alternative
    return val
