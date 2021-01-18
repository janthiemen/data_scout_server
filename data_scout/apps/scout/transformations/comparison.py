from apps.scout.transformations.transformation import Transformation


def convert_value(search, example):
    if isinstance(example, int):
        return int(search)
    elif isinstance(example, float):
        return float(search)
    return search


class CompareValue(Transformation):
    title = "Check if {field} {comparison} {value}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "comparison": {"name": "Comparison", "type": "string", "help": "How should the values be compared?",
                       "required": True, "input": "select", "multiple": False, "default": "==",
                       "options": {"==": "==", ">=": ">=", ">": ">", "<=": "<=", "<": "<", "!=": "!=", "in": "in"}},
        "value": {"name": "Value", "type": "string", "help": "The value to compare against",
                  "required": True, "input": "text", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        self.field = arguments["field"]
        self.comparison = arguments["comparison"]
        self.value = convert_value(arguments["value"], example[self.field])
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        if self.comparison == "==":
            row[self.output] = row[self.field] == self.value
        elif self.comparison == ">=":
            row[self.output] = row[self.field] >= self.value
        elif self.comparison == ">":
            row[self.output] = row[self.field] > self.value
        elif self.comparison == "<=":
            row[self.output] = row[self.field] <= self.value
        elif self.comparison == "<":
            row[self.output] = row[self.field] < self.value
        elif self.comparison == "!=":
            row[self.output] = row[self.field] != self.value
        elif self.comparison == "in":
            row[self.output] = self.value in row[self.field]

        return row, index


class CompareColumns(Transformation):
    title = "Check if {field_a} {comparison} {field_b}"
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
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to check",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "parity": {"name": "Parity", "type": "string", "help": "Even or odd",
                   "required": True, "input": "select", "multiple": False, "default": "==",
                   "options": {"even": "even", "odd": "odd"}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        self.field = arguments["field"]
        self.parity = arguments["parity"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        if self.parity == "even":
            row[self.output] = row[self.field] % 2 == 0
        else:
            row[self.output] = row[self.field] % 2 != 0

        return row, index


class Negate(Transformation):
    title = "Negate {field}"
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
    title = "Compare {fields} using {operator}"
    fields = {
        "fields": {"name": "Inputs", "type": "list<string>", "help": "The columns to use as input",
                   "required": True, "input": "column", "multiple": True, "default": ""},
        "operator": {"name": "Operator", "type": "string", "help": "How should the values be compared?",
                     "required": True, "input": "select", "multiple": False, "default": "==",
                     "options": {"and": "and", "or": "or", "xor": "xor"}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
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


class Min(Transformation):
    title = "Get the minimum of {fields}"
    fields = {
        "fields": {"name": "Inputs", "type": "list<string>", "help": "The columns to use as input",
                   "required": True, "input": "column", "multiple": True, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        self.fields = arguments["fields"]
        self.output = arguments["output"]

    def _get_values(self, row):
        return [row[field] for field in self.fields if field in row]

    def __call__(self, row, index: int):
        try:
            values = self._get_values(row)
            row[self.output] = min(values)
        except:
            row[self.output] = None
        return row, index


class Max(Min):
    title = "Get the maximum of {fields}"

    def __call__(self, row, index: int):
        try:
            values = self._get_values(row)
            row[self.output] = max(values)
        except:
            row[self.output] = None
        return row, index


class Mean(Min):
    title = "Get the mean of {fields}"

    def __call__(self, row, index: int):
        try:
            values = self._get_values(row)
            row[self.output] = sum(values) / len(values)
        except:
            row[self.output] = None
        return row, index


class Mode(Min):
    title = "Get the mode of {fields}"

    def __call__(self, row, index: int):
        try:
            values = self._get_values(row)
            row[self.output] = max(set(values), key=values.count)
        except:
            row[self.output] = None
        return row, index


class Coalesce(Min):
    title = "Get the first non-null value of {fields}"

    def __call__(self, row, index: int):
        try:
            row[self.output] = next(filter(None, self._get_values(row)))
        except:
            row[self.output] = None

        return row, index
