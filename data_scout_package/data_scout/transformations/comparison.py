import math

from .transformation import Transformation
from ._utils import compare_basis, compare_convert_value


class CompareValue(Transformation):
    title = "Check if {field} {comparison} {value}"
    key = "Compare to value"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
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
        row[self.output] = compare_basis(row[self.field], self.comparison, self.value)

        return row, index


class CompareColumns(Transformation):
    title = "Check if {field_a} {comparison} {field_b}"
    key = "Compare columns"
    fields = {
        "field_a": {"name": "Field A", "type": "string", "help": "The column on the left side",
                    "required": True, "input": "column", "multiple": False, "default": ""},
        "comparison": {"name": "Comparison", "type": "string", "help": "How should the values be compared?",
                       "required": True, "input": "select", "multiple": False, "default": "==",
                       "options": {"==": "==", ">=": ">=", ">": ">", "<=": "<=", "<": "<", "!=": "!=", "in": "in"}},
        "field_b": {"name": "Field B", "type": "string", "help": "The column on the right side",
                    "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field_a = arguments["field_a"]
        self.comparison = arguments["comparison"]
        self.field_b = arguments["field_b"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        if self.comparison == "==":
            row[self.output] = row[self.field_a] == row[self.field_b]
        elif self.comparison == ">=":
            row[self.output] = row[self.field_a] >= row[self.field_b]
        elif self.comparison == ">":
            row[self.output] = row[self.field_a] > row[self.field_b]
        elif self.comparison == "<=":
            row[self.output] = row[self.field_a] <= row[self.field_b]
        elif self.comparison == "<":
            row[self.output] = row[self.field_a] < row[self.field_b]
        elif self.comparison == "!=":
            row[self.output] = row[self.field_a] != row[self.field_b]
        elif self.comparison == "in":
            row[self.output] = row[self.field_a] in row[self.field_b]

        return row, index


class Parity(Transformation):
    title = "Check if {field} is {parity}"
    key = "Parity (even/odd)"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to check", "required": True, "input": "column",
                  "multiple": False, "default": "", "column_type": ["int", "float"]},
        "parity": {"name": "Parity", "type": "string", "help": "Even or odd",
                   "required": True, "input": "select", "multiple": False, "default": "==",
                   "options": {"even": "even", "odd": "odd"}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.parity = arguments["parity"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        if self.parity == "even":
            row[self.output] = row[self.field] % 2 == 0
        else:
            row[self.output] = row[self.field] % 2 != 0

        return row, index


class Mismatched(Transformation):
    title = "Check if {field} is mismatched"
    key = "Check mismatched"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to check",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = self.field not in row or row[self.field] is math.nan
        return row, index


class Missing(Mismatched):
    title = "Check if {field} is missing"
    key = "Check missing"

    def __call__(self, row, index: int):
        row[self.output] = self.field not in row or row[self.field] is None or \
                           row[self.field] is math.nan or \
                           (hasattr(row[self.field], '__len__') and len(row[self.field]) == 0)
        return row, index


class IsNull(Mismatched):
    title = "Check if {field} is null"
    key = "Check null"

    def __call__(self, row, index: int):
        row[self.output] = row[self.field] is None
        return row, index


class Negate(Transformation):
    title = "Negate {field}"
    key = "Negate"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to negate",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = not row[self.field]
        return row, index


class Logical(Transformation):
    title = "Compare {fields} using {comparison}"
    key = "Logical comparison (and/or/xor)"
    fields = {
        "fields": {"name": "Inputs", "type": "list<string>", "help": "The columns to use as input",
                   "required": True, "input": "column", "multiple": True, "default": ""},
        "comparison": {"name": "Comparison", "type": "string", "help": "How should the values be compared?",
                       "required": True, "input": "select", "multiple": False, "default": "and",
                       "options": {"and": "and", "or": "or", "xor": "xor"}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.comparison = arguments["comparison"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        if self.comparison == "and":
            row[self.output] = sum([not bool(row[field]) for field in self.fields]) == 0
        elif self.comparison == "or":
            row[self.output] = sum([bool(row[field]) for field in self.fields]) > 0
        elif self.comparison == "xor":
            row[self.output] = sum([bool(row[field]) for field in self.fields]) == 1

        return row, index


class IfElse(Transformation):
    title = "If else statement using {if}"
    key = "If/else"
    fields = {
        "field": {"name": "If", "type": "list<string>", "help": "The column that is used in the if statement (boolean)",
                  "column_type": ["bool"], "required": True, "input": "column", "multiple": True, "default": ""},
        "if_value_type": {"name": "If value type", "type": "string", "help": "What type of value should be used?",
                          "required": True, "input": "select", "multiple": False, "default": "column",
                          "options": {"column": "column", "string": "string", "integer": "integer", "float": "float"}},
        "if_value_column": {"name": "If value column", "type": "string", "required": False, "input": "column",
                            "help": "The column that is used as the value when the if statement evaluates to true",
                            "multiple": False, "default": "", "optional": {"if_value_type": ["column"]}},
        "if_value_string": {"name": "If value (string)", "type": "string", "input": "text", "required": False,
                            "help": "The value that is used when the if statement evaluates to true", "default": "",
                            "optional": {"if_value_type": ["string"]}},
        "if_value_number": {"name": "If value (number)", "type": "number", "input": "number", "required": False,
                            "help": "The value that is used when the if statement evaluates to true", "default": "",
                            "optional": {"if_value_type": ["int", "float"]}},
        "else_value_type": {"name": "Else value type", "type": "string", "help": "What type of value should be used?",
                            "required": True, "input": "select", "multiple": False, "default": "column",
                            "options": {"column": "column", "string": "string", "integer": "integer", "float": "float"}
                            },
        "else_value_column": {"name": "Else value column", "type": "string", "required": False, "input": "column",
                              "help": "The column that is used as the value when the if statement evaluates to false",
                              "multiple": False, "default": "", "optional": {"else_value_type": ["column"]}},
        "else_value_string": {"name": "Else value (string)", "type": "string", "input": "text", "required": False,
                              "help": "The value that is used when the if statement evaluates to false", "default": "",
                              "optional": {"else_value_type": ["string"]}},
        "else_value_number": {"name": "Else value (number)", "type": "number", "input": "number", "required": False,
                              "help": "The value that is used when the if statement evaluates to false", "default": "",
                              "optional": {"else_value_type": ["int", "float"]}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def _get_value(self, value_type, value_string, value_number):
        if value_type == "string":
            return str(value_string)
        elif value_type == "integer":
            return int(value_number)
        elif value_type == "float":
            return float(value_number)

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.if_is_column = arguments["if_value_type"] == "column"
        self.if_value = self._get_value(arguments["if_value_type"], arguments["if_value_string"],
                                        arguments["if_value_number"])
        self.if_column = arguments["if_value_column"]
        self.else_is_column = arguments["else_value_type"] == "column"
        self.else_value = self._get_value(arguments["else_value_type"], arguments["else_value_string"],
                                          arguments["else_value_number"])
        self.else_column = arguments["else_value_column"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        if row[self.field]:
            row[self.output] = row.get(self.if_column) if self.if_is_column else self.if_value
        else:
            row[self.output] = row.get(self.else_column) if self.else_is_column else self.else_value
        return row, index


class Min(Transformation):
    title = "Get the minimum of {fields}"
    key = "Columns minimum"
    fields = {
        "fields": {"name": "Inputs", "type": "list<string>", "help": "The columns to use as input",
                   "required": True, "input": "column", "multiple": True, "default": "",
                   "column_type": ["int", "float"]},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.output = arguments["output"]

    def _get_values(self, row):
        return [row[field] for field in self.fields if field in row]

    def __call__(self, row, index: int):
        try:
            values = self._get_values(row)
            row[self.output] = min(values)
        except:
            row[self.output] = math.nan
        return row, index


class Max(Min):
    title = "Get the maximum of {fields}"
    key = "Columns maximum"

    def __call__(self, row, index: int):
        try:
            values = self._get_values(row)
            row[self.output] = max(values)
        except:
            row[self.output] = math.nan
        return row, index


class Mean(Min):
    title = "Get the mean of {fields}"
    key = "Columns mean"

    def __call__(self, row, index: int):
        try:
            values = self._get_values(row)
            row[self.output] = sum(values) / len(values)
        except:
            row[self.output] = math.nan
        return row, index


class Mode(Min):
    title = "Get the mode of {fields}"
    key = "Columns mode"

    def __call__(self, row, index: int):
        try:
            values = self._get_values(row)
            row[self.output] = max(set(values), key=values.count)
        except:
            row[self.output] = math.nan
        return row, index


class Coalesce(Min):
    title = "Get the first non-null value of {fields}"
    key = "Columns coalesce"

    def __call__(self, row, index: int):
        try:
            row[self.output] = next(filter(None, self._get_values(row)))
        except:
            row[self.output] = None

        return row, index
