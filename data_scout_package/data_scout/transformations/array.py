import itertools
import math
import statistics
from typing import List, Tuple

from .transformation import Transformation
from ._utils import compare_basis, compare_convert_value


def convert_value(search, example):
    if isinstance(example, list):
        example = example[0]

    if isinstance(example, int):
        return int(search)
    elif isinstance(example, float):
        return float(search)
    elif isinstance(example, bool):
        return bool(search)

    return search


class Index(Transformation):
    title = "Get the {side} index of {value} in the list {field} (-1 if not found)"
    key = "Array index"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to use", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "value": {"name": "Value", "type": "string", "input": "text", "required": True,
                  "help": "The value to look for", "default": ""},
        "side": {"name": "Side", "type": "string", "help": "Do you want the index of the first or the last occurrence?",
                 "required": True, "input": "select", "multiple": False, "default": "first",
                 "options": {"first": "First", "last": "Last"}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.value = convert_value(arguments["value"], example[self.field])
        self.side = arguments["side"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            if self.side == "last":
                row[self.output] = len(row[self.field]) - row[self.field][::-1].index(self.value) - 1
            else:
                row[self.output] = row[self.field].index(self.value)
        except:
            row[self.output] = -1
        return row, index


class AtIndex(Transformation):
    title = "Get the element at zero-based index {index} from {field}"
    key = "Array at index"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to use", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "index": {"name": "Index", "type": "number", "input": "number", "required": True,
                  "help": "The zero-based index of the element you want to retrieve", "default": 0},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.index = arguments["index"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = row[self.field][self.index]
        except:
            row[self.output] = None
        return row, index


class Slice(Transformation):
    title = "Slice the list in {field} from {start} to {end}"
    key = "Array slice"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to use", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "start": {"name": "Start", "type": "number", "help": "The start index (0 to start at the beginning)",
                  "required": True, "input": "number", "default": 0},
        "end": {"name": "End", "type": "number", "required": False, "input": "number", "default": "",
                "help": "The end index (can be left empty, -2 means stop two elements from the end)"},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.start = arguments["start"]

        self.end = arguments["end"]
        if len(str(self.end)) > 0:
            self.end = int(self.end)
        else:
            self.end = None

        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = row[self.field][self.start:self.end]
        except:
            row[self.output] = []
        return row, index


class Length(Transformation):
    title = "Get the length of the list in {field}"
    key = "Array length"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to use", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = len(row[self.field])
        except:
            row[self.output] = 0
        return row, index


class Mean(Transformation):
    title = "Get the mean of the list in {field}"
    key = "Array mean"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to use", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = sum(row[self.field]) / len(row[self.field])
        except:
            row[self.output] = math.nan
        return row, index


class Sum(Transformation):
    title = "Get the mean of the list in {field}"
    key = "Array sum"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to use", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = sum(row[self.field])
        except:
            row[self.output] = math.nan
        return row, index


class Min(Transformation):
    title = "Get the min of the list in {field}"
    key = "Array min"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to use", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = min(row[self.field])
        except:
            row[self.output] = math.nan
        return row, index


class Max(Transformation):
    title = "Get the max of the list in {field}"
    key = "Array max"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to use", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = max(row[self.field])
        except:
            row[self.output] = math.nan
        return row, index


class Mode(Transformation):
    title = "Get the mode of the list in {field}"
    key = "Array mode"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to use", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = max(set(row[self.field]), key=row[self.field].count)
        except:
            row[self.output] = math.nan
        return row, index


class Std(Transformation):
    title = "Get the standard deviation of the list in {field}"
    key = "Array standard deviation (std)"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to use", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = statistics.stdev(row[self.field])
        except:
            row[self.output] = math.nan
        return row, index


class Var(Transformation):
    title = "Get the variance of the list in {field}"
    key = "Array variance (var)"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to use", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = statistics.variance(row[self.field])
        except:
            row[self.output] = math.nan
        return row, index


class Sort(Transformation):
    title = "Sort the values of the list in {field}"
    key = "Array sort"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to use", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "order": {"name": "Order", "type": "string", "help": "Should the values be sorted ascending or descending?",
                  "required": True, "input": "select", "multiple": False, "default": "asc",
                  "options": {"asc": "Ascending", "desc": "Descending"}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.reverse = arguments["order"] == "desc"
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = sorted(row[self.field], reverse=self.reverse)
        except:
            row[self.output] = None
        return row, index


class Concat(Transformation):
    title = "Concat the arrays in {fields}"
    key = "Array concat"
    fields = {
        "fields": {"name": "Inputs", "type": "list<string>", "help": "The columns to use as input",
                   "required": True, "input": "column", "multiple": True, "default": "", "column_type": ["list"]},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = list(itertools.chain.from_iterable([row.get(field, []) for field in self.fields]))
        except:
            row[self.output] = []
        return row, index


class Intersect(Transformation):
    title = "Get the intersection of the in {fields}"
    key = "Array intersect"
    fields = {
        "fields": {"name": "Inputs", "type": "list<string>", "help": "The columns to use as input",
                   "required": True, "input": "column", "multiple": True, "default": "", "column_type": ["list"]},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            lists = [row.get(field, []) for field in self.fields if field in row]
            if len(lists) == 0:
                row[self.output] = []
            elif len(lists) == 1:
                row[self.output] = lists[0]
            else:
                row[self.output] = set(lists[0]).intersection(*lists[1:])
        except:
            row[self.output] = []
        return row, index


class Unique(Transformation):
    title = "Get all unique elements in {fields}"
    key = "Array unique"
    fields = {
        "fields": {"name": "Inputs", "type": "list<string>", "help": "The columns to use as input",
                   "required": True, "input": "column", "multiple": True, "default": "", "column_type": ["list"]},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = list(set(itertools.chain.from_iterable([row.get(field, []) for field in self.fields])))
        except:
            row[self.output] = []
        return row, index


class Filter(Transformation):
    title = "Filter all elements from list where {field}[x] {comparison} {value}"
    key = "Array filter"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "comparison": {"name": "Comparison", "type": "string", "help": "How should the values be compared?",
                       "required": True, "input": "select", "multiple": False, "default": "==",
                       "options": {"==": "==", ">=": ">=", ">": ">", "<=": "<=", "<": "<", "!=": "!=",
                                   "in": "in (value in column)", "in_list": "in list (column in list of values)"}},
        "value": {"name": "Value", "type": "string", "required": True, "input": "text-area", "default": "",
                  "help": "The value to compare against (one per line to create a list)"},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.comparison = arguments["comparison"]
        self.value = compare_convert_value(arguments["value"].splitlines(), example[self.field])
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = filter(lambda x: compare_basis(x, self.comparison, self.value), row[self.field])
        except:
            row[self.output] = []
        return row, index


class Flatten(Transformation):
    title = "Flatten {field}"
    key = "Array flatten"
    is_flatten = True
    fields = {
        "field": {"name": "Field", "type": "string", "required": True,
                  "help": "The field that should be flattened. This will create one row for each element in the list",
                  "input": "column", "multiple": False, "default": "", "column_type": ["list"]},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]

    def __call__(self, row, index: int) -> Tuple[List[dict], int]:
        if self.field not in row or not isinstance(row[self.field], list):
            return [row], index

        rows = []
        if len(row[self.field]) == 0:
            row[self.field] = math.nan
            rows.append(row)
        else:
            for i, val in enumerate(row[self.field]):
                row_tmp = row.copy()
                row_tmp[self.field] = val
                rows.append(row_tmp)

        return rows, index


class ToDict(Transformation):
    title = "Combine an array keys ({field_keys}) and values ({field_values}) into a dictionary."
    key = "Array to dictionary"
    fields = {
        "field_keys": {"name": "Keys", "type": "string", "column_type": ["list"], "required": True, "input": "column",
                       "help": "The array containing the keys", "multiple": False, "default": ""},
        "field_values": {"name": "Values", "type": "string", "column_type": ["list"], "required": True,
                         "help": "The array containing the values", "input": "column", "multiple": False,
                         "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field_keys = arguments["field_keys"]
        self.field_values = arguments["field_values"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = dict(zip(row[self.field_keys], row[self.field_values]))
        return row, index


class Merge(Transformation):
    title = "Merge the elements of the list in {field} together, separated by {separator}"
    key = "Array merge"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input", "column_type": ["list"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "separator": {"name": "Separator", "type": "string", "help": "The separator between the different values",
                      "required": True, "input": "text", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.separator = arguments["separator"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = self.separator.join(row[self.field])
        except:
            row[self.output] = ""
        return row, index
