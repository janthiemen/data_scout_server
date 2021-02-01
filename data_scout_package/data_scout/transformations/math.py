from .transformation import Transformation


class Add(Transformation):
    title = "Sum {fields}"
    key = "Math add"
    fields = {
        "fields": {"name": "Columns", "type": "list<string>", "help": "The fields to add to each other",
                   "required": True, "input": "column", "multiple": True, "default": "",
                   "column_type": ["int", "float"]},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        total = 0
        for field in [f for f in self.fields if f in row]:
            total += row[field]

        row[self.output] = total
        return row, index


class Min(Transformation):
    title = "Calculate {field_a} - {field_b}"
    key = "Math min"
    fields = {
        "field_a": {"name": "Field 1", "type": "string", "help": "The field that should be subtracted from",
                    "required": True, "input": "column", "multiple": False, "default": "",
                    "column_type": ["int", "float"]},
        "field_b": {"name": "Field 2", "type": "string", "help": "The field that should be subtracted",
                    "required": True, "input": "column", "multiple": False, "default": "",
                    "column_type": ["int", "float"]},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field_a = arguments["field_a"]
        self.field_b = arguments["field_b"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        if self.field_a not in row or self.field_b not in row:
            return row, index

        row[self.output] = row[self.field_a] - row[self.field_b]
        return row, index


class Divide(Transformation):
    title = "Calculate {field_a} / {field_b}"
    key = "Math divide"
    fields = {
        "field_a": {"name": "Numerator", "type": "string", "help": "The numerator", "required": True, "input": "column",
                    "multiple": False, "default": "", "column_type": ["int", "float"]},
        "field_b": {"name": "Denominator", "type": "string", "help": "The denominator", "required": True,
                    "input": "column", "multiple": False, "default": "", "column_type": ["int", "float"]},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field_a = arguments["field_a"]
        self.field_b = arguments["field_b"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        # TODO: Add check on division by 0?
        if self.field_a not in row or self.field_b not in row:
            return row, index
        row[self.output] = row[self.field_a] / row[self.field_b]
        return row, index


class Multiply(Transformation):
    title = "Multiply {fields}"
    key = "Math multiply"
    fields = {
        "fields": {"name": "Fields", "type": "list<string>", "help": "The fields to add to each other",
                   "required": True, "input": "column", "multiple": True, "default": "",
                   "column_type": ["int", "float"]},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        total = None
        for field in [f for f in self.fields if f in row]:
            if total is None:
                total = row[field]
            else:
                total *= row[field]

        row[self.output] = total
        return row, index
