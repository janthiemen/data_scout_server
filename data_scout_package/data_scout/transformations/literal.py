import random

from .transformation import Transformation


# TODO: Should we combine all of these into one transformation?
class Literal(Transformation):
    fields = {
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        """Initialize the transformation with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        super().__init__(arguments, sample_size, example)
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        raise NotImplementedError


class String(Transformation):
    key = "String literal"
    title = "Create a string column {output} with the value {value}"
    fields = {
        "value": {"name": "Value", "type": "string", "input": "text", "required": True,
                  "help": "The value to populate the new column with", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.value = str(arguments["value"])
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = self.value
        return row, index


class Integer(Transformation):
    key = "Integer literal"
    title = "Create an integer column {output} with the value {value}"
    fields = {
        "value": {"name": "Value", "type": "number", "input": "number", "required": True,
                  "help": "The value to populate the new column with", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.value = int(arguments["value"])
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = self.value
        return row, index


class Float(Transformation):
    key = "Float literal"
    title = "Create a float column {output} with the value {value}"
    fields = {
        "value": {"name": "Value", "type": "number", "input": "number", "required": True,
                  "help": "The value to populate the new column with", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.value = float(arguments["value"])
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = self.value
        return row, index


class Null(Transformation):
    key = "Null literal"
    title = "Create a column {output} containing only null (None) values"
    fields = {
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = None
        return row, index


class RandBetween(Transformation):
    key = "Random float between"
    title = "Create a float column {output} with a random value between {start} and {end}"
    fields = {
        "start": {"name": "From", "type": "number", "input": "number", "required": True,
                  "help": "The lower bound for the random number generator", "default": 0.0},
        "end": {"name": "Till", "type": "number", "input": "number", "required": True,
                "help": "The upper bound for the random number generator", "default": 1.0},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.start = float(arguments["start"])
        self.end = float(arguments["end"])
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = random.uniform(self.start, self.end)
        return row, index


class RandInt(Transformation):
    key = "Random integer between"
    title = "Create an integer column {output} with a random value between {start} and {end}"
    fields = {
        "start": {"name": "From", "type": "number", "input": "number", "required": True,
                  "help": "The lower bound for the random number generator", "default": 0},
        "end": {"name": "Till", "type": "number", "input": "number", "required": True,
                "help": "The upper bound for the random number generator", "default": 10},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.start = int(arguments["start"])
        self.end = int(arguments["end"])
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = random.randrange(self.start, self.end)
        return row, index
