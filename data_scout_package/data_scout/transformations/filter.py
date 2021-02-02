import math
import re
import pandas as pd
from pandas.core.dtypes.inference import is_hashable

from .transformation import Transformation
from ..exceptions import IndexFilterException


class FilterMissing(Transformation):
    filter = True
    title = "Filter rows with missing values in {field}"
    key = "Filter missing values"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]

    def __call__(self, row, index: int):
        if self.field not in row or pd.isnull(row[self.field]) or \
                (hasattr(row[self.field], '__len__') and len(row[self.field]) == 0):
            return False, index

        return row, index


class FilterMismatched(Transformation):
    filter = True
    title = "Filter rows with mismatched values in {field}"
    key = "Filter mismatched values"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]

    def __call__(self, row, index: int):
        if self.field not in row or row[self.field] is math.nan:
            return False, index

        return row, index


def convert_search_value(search, example):
    if isinstance(example, int):
        return int(search)
    elif isinstance(example, float):
        return float(search)
    return search


class FilterIs(Transformation):
    filter = True
    title = "Filter rows where {field} matched {search}"
    key = "Filter were equals"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The string to search for",
                   "required": True, "input": "text", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.search = convert_search_value(arguments["search"], example[self.field])

    def __call__(self, row, index: int):
        if self.field in row and row[self.field] == self.search:
            return False, index

        return row, index


class FilterIsNot(Transformation):
    filter = True
    title = "Filter rows where {field} does not equal {search}"
    key = "Filter where not equals"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The string to search for",
                   "required": True, "input": "text", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.search = convert_search_value(arguments["search"], example[self.field])

    def __call__(self, row, index: int):
        if self.field not in row or row[self.field] != self.search:
            return False, index

        return row, index


class FilterList(Transformation):
    filter = True
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The values to search for (one per line)",
                   "required": True, "input": "text-area", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.search = arguments["search"].splitlines()
        if isinstance(example[self.field], int):
            self.search = [int(item) for item in self.search]
        elif isinstance(example[self.field], float):
            self.search = [float(item) for item in self.search]

    def __call__(self, row, index: int):
        raise NotImplemented


class FilterIsOneOf(FilterList):
    title = "Filter rows where {field} is one of {self.search}"
    key = "Filter where in list"

    def __call__(self, row, index: int):
        if self.field in row and row[self.field] in self.search:
            return False, index

        return row, index


class FilterIsnotOneOf(FilterList):
    title = "Filter rows where {field} is not one of {self.search}"
    key = "Filter where not in list"

    def __call__(self, row, index: int):
        if self.field not in row or row[self.field] not in self.search:
            return False, index

        return row, index


class FilterLessThan(Transformation):
    filter = True
    title = "Filter rows where {field} is lower than {threshold}"
    key = "Filter lower than"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "threshold": {"name": "Threshold", "type": "number", "help": "The threshold value",
                      "required": True, "input": "number", "multiple": False, "default": 0},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.threshold = convert_search_value(arguments["threshold"], example[self.field])

    def __call__(self, row, index: int):
        if self.field in row and row[self.field] < self.threshold:
            return False, index

        return row, index


class FilterGreaterThan(Transformation):
    filter = True
    title = "Filter rows where {field} is higher than {threshold}"
    key = "Filter greater than"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "threshold": {"name": "Threshold", "type": "number", "help": "The threshold value",
                      "required": True, "input": "number", "multiple": False, "default": 0},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.threshold = convert_search_value(arguments["threshold"], example[self.field])

    def __call__(self, row, index: int):
        if self.field in row and row[self.field] > self.threshold:
            return False, index

        return row, index


class FilterBetween(Transformation):
    filter = True
    title = "Filter rows where {field} is between {min} and {max}"
    key = "Filter between"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "min": {"name": "Min", "type": "number", "help": "The bottom of the range",
                "required": True, "input": "number", "multiple": False, "default": 0},
        "max": {"name": "Max", "type": "number", "help": "The top of the range",
                "required": True, "input": "number", "multiple": False, "default": 0},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.min = convert_search_value(arguments["min"], example[self.field])
        self.max = convert_search_value(arguments["max"], example[self.field])

    def __call__(self, row, index: int):
        if self.field in row and self.min < row[self.field] < self.max:
            return False, index

        return row, index


class FilterNotBetween(Transformation):
    filter = True
    title = "Filter rows where {field} is not between {min} and {max}"
    key = "Filter not between"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "min": {"name": "Min", "type": "number", "help": "The bottom of the range",
                "required": True, "input": "number", "multiple": False, "default": 0},
        "max": {"name": "Max", "type": "number", "help": "The top of the range",
                "required": True, "input": "number", "multiple": False, "default": 0},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.min = convert_search_value(arguments["min"], example[self.field])
        self.max = convert_search_value(arguments["max"], example[self.field])

    def __call__(self, row, index: int):
        if self.field not in row or self.min < row[self.field] < self.max:
            return False, index

        return row, index


class FilterContains(Transformation):
    filter = True
    title = "Filter rows where {field} contains {search}"
    key = "Filter contains"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The string to search for",
                   "required": True, "input": "text", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.search = arguments["search"]

    def __call__(self, row, index: int):
        if self.field in row and self.search in row[self.field]:
            return False, index

        return row, index


class FilterStartsWith(Transformation):
    filter = True
    title = "Filter rows where {field} starts with {search}"
    key = "Filter starts with"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The string to search for",
                   "required": True, "input": "text", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.search = arguments["search"]

    def __call__(self, row, index: int):
        if self.field in row and str(row[self.field]).startswith(self.search):
            return False, index

        return row, index


class FilterEndsWith(Transformation):
    filter = True
    title = "Filter rows where {field} ends with {search}"
    key = "Filter ends with"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The string to search for",
                   "required": True, "input": "text", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.search = arguments["search"]

    def __call__(self, row, index: int):
        if self.field in row and str(row[self.field]).endswith(self.search):
            return False, index

        return row, index


class FilterRegex(Transformation):
    filter = True
    title = "Filter rows where {field} matches {search}"
    key = "Filter regex"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The regex pattern to match",
                   "required": True, "input": "text", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.search = re.compile(arguments["search"])

    def __call__(self, row, index: int):
        if self.field in row and self.search.match(str(row[self.field])):
            return False, index

        return row, index


class FilterRowsInterval(Transformation):
    filter = True
    title = "Filter the rows at a regular interval of {interval}"
    key = "Filter at interval"
    allowed_sampling_techniques = ["top"]
    fields = {
        "interval": {"name": "Interval", "type": "number", "help": "The interval at which to sample",
                     "required": True, "input": "number", "multiple": False, "default": 2},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.interval = arguments["interval"]
        if self.interval < 2:
            raise IndexFilterException(f"We can't delete every {self.interval} rows, as it would delete all rows in the sample.")

    def __call__(self, row, index: int):
        if index % self.interval == 0:
            return False, index

        return row, index


class FilterRowsRange(Transformation):
    filter = True
    title = "Filter the rows in the range {min} - {max}"
    key = "Filter in range"
    allowed_sampling_techniques = ["top"]
    fields = {
        "min": {"name": "Min", "type": "number", "help": "The bottom of the range",
                "required": True, "input": "number", "multiple": False, "default": 0},
        "max": {"name": "Max", "type": "number", "help": "The top of the range",
                "required": True, "input": "number", "multiple": False, "default": 0},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.min = arguments["min"]
        self.max = arguments["max"]
        if self.max >= sample_size and self.min < 1:
            raise IndexFilterException(f"We couldn't delete the in the range {self.min} - {self.max}, as it would delete all rows in the sample. The transformation was skipped but will be performed in a non-sampled environment.")

    def __call__(self, row, index: int):
        if self.min <= index <= self.max:
            return False

        return row, index


class FilterRowsTop(Transformation):
    filter = True
    title = "Filter the top {rows} rows"
    key = "Filter top rows"
    allowed_sampling_techniques = ["top"]
    fields = {
        "rows": {"name": "Rows", "type": "number", "help": "The number of rows to filter out from the top",
                 "required": True, "input": "number", "multiple": False, "default": 0},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.rows = arguments["rows"]
        if sample_size <= self.rows:
            raise IndexFilterException(f"We couldn't delete the top {self.rows} rows, as it would delete all rows in the sample. The transformation was skipped but will be performed in a non-sampled environment.")

    def __call__(self, row, index: int):
        if index <= self.rows:
            return False

        return row, index


class FilterRowsDuplicates(Transformation):
    is_global = True
    title = "Filter the duplicates from the dataset"
    key = "Filter duplicate rows"
    fields = {
        "fields": {"name": "Fields", "type": "list<string>", "help": "The fields to check",
                   "required": True, "input": "column", "multiple": True, "default": "",
                   "column_types": ["str", "int", "float", "datetime"]},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]

    def __call__(self, rows: pd.DataFrame, index: int):
        for field in self.fields:
            if not is_hashable(rows[field].iloc[0]):
                raise TypeError(f"The column type of {field} can't be checked for duplicates")
        return rows.drop_duplicates(subset=self.fields).to_dict(orient="records"), index
        # seen = set()
        # seen_add = seen.add
        # filtered_rows = []
        # for row in rows:
        #     test = frozenset([row[key] for key in self.fields if key in row])
        #     if not (test in seen or seen_add(test)):
        #         filtered_rows.append(row)
        # # TODO: Check what happens here in Spark/how to handle this
        # return filtered_rows, index
