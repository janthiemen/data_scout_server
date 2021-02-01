import re
import base64

from .transformation import Transformation


class Substring(Transformation):
    title = "Extract a substring from the left of length {right} from {field} into {output}"
    key = "Substring"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "left": {"name": "Start", "type": "number", "help": "The start index",
                 "required": True, "input": "number", "multiple": False, "default": 0},
        "right": {"name": "End", "type": "number", "help": "The end index",
                  "required": True, "input": "number", "multiple": False, "default": 0},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.left = arguments["left"]
        self.right = arguments["right"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = str(row[self.field])[self.left:self.right]
        return row, index


class SubstringLeft(Substring):
    title = "Extract a substring from the left of length {right} from {field} into {output}"
    key = "Substring left"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "right": {"name": "Length", "type": "number", "help": "The number of characters to select",
                  "required": True, "input": "number", "multiple": False, "default": 0},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        arguments["left"] = 0
        super().__init__(arguments, sample_size, example)


class SubstringRight(Substring):
    title = "Extract a substring from the right of length {left} from {field} into {output}"
    key = "Substring right"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "left": {"name": "Length", "type": "number", "help": "The number of characters to select",
                 "required": True, "input": "number", "multiple": False, "default": 0},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        arguments["right"] = None
        super().__init__(arguments, sample_size, example)


class FindLeft(Transformation):
    title = "Find the index of the first occurrence of {lookup} in {field} into {output} (left to right)"
    key = "String find left"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "lookup": {"name": "Input", "type": "string", "help": "The text to look for",
                   "required": True, "input": "text", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.lookup = arguments["lookup"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = str(row[self.field]).find(row[self.lookup])
        return row, index


class FindRight(FindLeft):
    title = "Find the index of the first occurrence of {lookup} in {field} into {output} (right to left)"
    key = "String find right"

    def __call__(self, row, index: int):
        row[self.output] = str(row[self.field]).rfind(row[self.lookup])
        return row, index


class Length(Transformation):
    title = "Calculate the length of {field} into {output}"
    key = "String length"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = len(row[self.field])
        return row, index


class Merge(Transformation):
    title = "Merge string columns together, with the separator {separator}"
    key = "String merge"
    fields = {
        "fields": {"name": "Inputs", "type": "list<string>", "help": "The columns to use as input",
                   "required": True, "input": "column", "multiple": True, "default": ""},
        "separator": {"name": "Separator", "type": "string", "help": "The separator between the different values",
                      "required": True, "input": "text", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.separator = arguments["separator"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = self.separator.join([row.get(f) for f in self.fields])
        return row, index


class Repeat(Transformation):
    title = "Repeat the value in {field} {times} times into {output}"
    key = "String repeat"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "times": {"name": "Times", "type": "number", "help": "The number of times to repeat the text",
                  "required": True, "input": "number", "multiple": False, "default": 0},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.times = arguments["times"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = str(row[self.field]) * int(self.times)
        return row, index


class TestContains(Transformation):
    title = "Test if {field} contains {search} into {output}"
    key = "String contains"
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
        row[self.output] = self.field in row and self.search in row[self.field]
        return row, index


class TestStartsWith(Transformation):
    title = "Test if {field} starts with {search} into {output}"
    key = "String starts with"
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
        row[self.output] = self.field in row and str(row[self.field]).startswith(self.search)
        return row, index


class TestEndsWith(Transformation):
    title = "Test if {field} ends with {search} into {output}"
    key = "String ends with"
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
        row[self.output] = self.field in row and str(row[self.field]).endswith(self.search)
        return row, index


class TestRegex(Transformation):
    title = "Test if {field} matches {regex} into {output}"
    key = "String regex"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "regex": {"name": "Regex", "type": "string", "help": "The regex to check against",
                  "required": True, "input": "text", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.regex = re.compile(arguments["regex"])
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = self.field in row and self.regex.match(str(row[self.field]))
        return row, index

# TODO: Can we replace all of these by the one comparison transform?


class TestExact(Transformation):
    title = "Test if {field} == {search} into {output}"
    key = "String equals"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The value to test against",
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
        row[self.output] = self.field in row and str(row[self.field]) == self.search
        return row, index


class TestGreater(Transformation):
    title = "Test if {field} > {search} into {output}"
    key = "String greater than"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The value to test against",
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
        row[self.output] = self.field in row and str(row[self.field]) > self.search
        return row, index


class TestGreaterEqual(Transformation):
    title = "Test if {field} >= {search} into {output}"
    key = "String greater or equal"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The value to test against",
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
        row[self.output] = self.field in row and str(row[self.field]) >= self.search
        return row, index


class TestLess(Transformation):
    title = "Test if {field} < {search} into {output}"
    key = "String less than"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The value to test against",
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
        row[self.output] = self.field in row and str(row[self.field]) < self.search
        return row, index


class TestLessEqual(Transformation):
    title = "Test if {field} <= {search} into {output}"
    key = "String less or equal"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "search": {"name": "Search", "type": "string", "help": "The value to test against",
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
        row[self.output] = self.field in row and str(row[self.field]) <= self.search
        return row, index


class Base64Encode(Transformation):
    title = "Base64 encode {field} into {output}"
    key = "Base64 encode"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = base64.b64encode(str(row[self.field]).encode('utf-8')).decode("utf-8")
        return row, index


class Base64Decode(Transformation):
    title = "Base64 decode {field} into {output}"
    key = "Base64 decode"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = base64.b64decode(str(row[self.field]).encode('utf-8')).decode('utf-8')
        return row, index
