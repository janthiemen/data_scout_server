import re

from .transformation import Transformation


class CountExact(Transformation):
    title = "Count exact matches of {search} in {field} as {output}"
    key = "Count string matches"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The string to search for",
                   "required": True, "input": "text", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.search = arguments["search"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        if self.field in row:
            row[self.output] = row[self.field].count(self.search)
        else:
            row[self.output] = 0

        return row, index


class CountRegex(Transformation):
    title = "Count exact matches of the regex {pattern} in {field} as {output}"
    key = "Count regex matches"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "pattern": {"name": "Pattern", "type": "regex", "help": "The regex pattern to look for",
                    "required": True, "input": "text", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.pattern = re.compile(arguments["pattern"])
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        # TODO: Check if the regex is correct
        if self.field in row:
            row[self.output] = len(re.findall(self.pattern, row[self.field]))
        else:
            row[self.output] = 0

        return row, index


class CountDelimiters(Transformation):
    title = "Count the number of strings between delimiter {delimiter} in {field} as {output}"
    key = "Count between delimiters"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "delimiter": {"name": "Delimiter", "type": "string", "help": "The delimiter to split the string on",
                      "required": True, "input": "text", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.delimiter = arguments["delimiter"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        # TODO: Check if the regex is correct
        if self.field in row:
            row[self.output] = row[self.field].count(self.delimiter) + 1
        else:
            row[self.output] = 0

        return row, index
