import math
import re

from apps.scout.transformations.transformation import Transformation


class FilterMissing(Transformation):
    filter = True
    title = "Filter rows with missing values in {field}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]

    def __call__(self, row):
        if row[self.field] is None or len(row[self.field]) == 0:
            return False

        return row


class FilterMismatched(Transformation):
    filter = True
    title = "Filter rows with mismatched values in {field}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
    }

    def __init__(self, arguments):
        self.field = arguments["field"]

    def __call__(self, row):
        if row[self.field] is math.nan:
            return False

        return row


def convert_search_value(search, example):
    if isinstance(example, int):
        return int(search)
    elif isinstance(example, float):
        return float(search)
    return search


class FilterIs(Transformation):
    filter = True
    title = "Filter rows where {field} matched {search}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The string to search for",
                   "required": True, "input": "text", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.search = convert_search_value(arguments["search"], example[self.field])

    def __call__(self, row):
        if row[self.field] == self.search:
            return False

        return row


class FilterIsNot(Transformation):
    filter = True
    title = "Filter rows where {field} does not equal {search}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The string to search for",
                   "required": True, "input": "text", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.search = convert_search_value(arguments["search"], example[self.field])

    def __call__(self, row):
        if row[self.field] != self.search:
            return False

        return row


class FilterList(Transformation):
    filter = True
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The values to search for (one per line)",
                   "required": True, "input": "text-area", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.search = arguments["search"].splitlines()
        if isinstance(example[self.field], int):
            self.search = [int(item) for item in self.search]
        elif isinstance(example[self.field], float):
            self.search = [float(item) for item in self.search]


class FilterIsOneOf(FilterList):
    title = "Filter rows where {field} is one of"

    def __call__(self, row):
        if row[self.field] in self.search:
            return False

        return row


class FilterIsnotOneOf(FilterList):
    title = "Filter rows where {field} is not one of"

    def __call__(self, row):
        if row[self.field] not in self.search:
            return False

        return row


class FilterLessThan(Transformation):
    filter = True
    title = "Filter rows where {field} is lower than {threshold}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "threshold": {"name": "Threshold", "type": "number", "help": "The threshold value",
                      "required": True, "input": "number", "multiple": False, "default": 0},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.threshold = convert_search_value(arguments["threshold"], example[self.field])

    def __call__(self, row):
        if row[self.field] < self.threshold:
            return False

        return row


class FilterGreaterThan(Transformation):
    filter = True
    title = "Filter rows where {field} is higher than {threshold}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "threshold": {"name": "Threshold", "type": "number", "help": "The threshold value",
                      "required": True, "input": "number", "multiple": False, "default": 0},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.threshold = convert_search_value(arguments["threshold"], example[self.field])

    def __call__(self, row):
        if row[self.field] > self.threshold:
            return False

        return row


class FilterBetween(Transformation):
    filter = True
    title = "Filter rows where {field} is between {min} and {max}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "min": {"name": "Min", "type": "number", "help": "The bottom of the range",
                "required": True, "input": "number", "multiple": False, "default": 0},
        "max": {"name": "Max", "type": "number", "help": "The top of the range",
                "required": True, "input": "number", "multiple": False, "default": 0},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.min = convert_search_value(arguments["min"], example[self.field])
        self.max = convert_search_value(arguments["max"], example[self.field])

    def __call__(self, row):
        if self.min < row[self.field] < self.max:
            return False

        return row


class FilterNotBetween(Transformation):
    filter = True
    title = "Filter rows where {field} is not between {min} and {max}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "min": {"name": "Min", "type": "number", "help": "The bottom of the range",
                "required": True, "input": "number", "multiple": False, "default": 0},
        "max": {"name": "Max", "type": "number", "help": "The top of the range",
                "required": True, "input": "number", "multiple": False, "default": 0},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.min = convert_search_value(arguments["min"], example[self.field])
        self.max = convert_search_value(arguments["max"], example[self.field])

    def __call__(self, row):
        if self.min < row[self.field] < self.max:
            return row

        return False


class FilterContains(Transformation):
    filter = True
    title = "Filter rows where {field} contains {search}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The string to search for",
                   "required": True, "input": "text", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.search = arguments["search"]

    def __call__(self, row):
        if self.search in row[self.field]:
            return False

        return row


class FilterStartsWith(Transformation):
    filter = True
    title = "Filter rows where {field} starts with {search}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The string to search for",
                   "required": True, "input": "text", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.search = arguments["search"]

    def __call__(self, row):
        if str(row[self.field]).startswith(self.search):
            return False

        return row


class FilterEndsWith(Transformation):
    filter = True
    title = "Filter rows where {field} ends with {search}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The string to search for",
                   "required": True, "input": "text", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.search = arguments["search"]

    def __call__(self, row):
        if str(row[self.field]).endswith(self.search):
            return False

        return row


class FilterRegex(Transformation):
    filter = True
    title = "Filter rows where {field} matches {search}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The regex pattern to match",
                   "required": True, "input": "text", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.search = re.compile(arguments["search"])

    def __call__(self, row):
        if self.search.match(str(row[self.field])):
            return False

        return row


