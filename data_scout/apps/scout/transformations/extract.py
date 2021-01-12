import math
import re
import urllib.parse as urlparse
from urllib.parse import parse_qs

from apps.scout.transformations.transformation import Transformation


class ExtractNumbers(Transformation):
    title = "Extract numbers from {field} into {output}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row):
        numbers = []
        for t in row[self.field].split():
            try:
                numbers.append(float(t))
            except ValueError:
                pass

        row[self.output] = numbers
        return row


class ExtractHttpQueryString(Transformation):
    title = "Extract HTTP query string from {field} into {output}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row):
        try:
            parsed = urlparse.urlparse(row[self.field])
            row[self.output] = parse_qs(parsed.query)
        except:
            row[self.output] = {}

        return row


class ExtractRegex(Transformation):
    title = "Extract regex from {field} into {output}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "pattern": {"name": "Pattern", "type": "regex", "help": "The regex pattern that should be extracted",
                    "required": True, "input": "text", "default": ""},
        # "group": {"name": "Pattern", "type": "integer", "help":
        #           "The group in the pattern to extract (0 for the whole match)", "required": True, "input": "text",
        #           "default": 0},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.pattern = re.compile(arguments["pattern"])
        self.output = arguments["output"]

    def __call__(self, row):
        try:
            row[self.output] = self.pattern.findall(row[self.field])
        except:
            row[self.output] = []

        return row


class ExtractDelimiters(ExtractRegex):
    title = "Extract the text between the delimiter: {delimiter} in {field} as {output}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "delimiter": {"name": "Delimiter", "type": "string", "help": "The delimiter to split the string on",
                      "required": True, "input": "text", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        arguments["pattern"] = '{delimiter}.*{delimiter}'.format(delimiter=arguments["delimiter"])
        super().__init__(arguments)
        self.pattern = re.compile(arguments["pattern"], flags=re.DOTALL)


class ExtractPositions(Transformation):
    title = "Extract the characters between pos. {start} - {end} into {output}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "start": {"name": "Start", "type": "int", "help": "The start position", "required": True, "input": "number",
                  "default": 0},
        "end": {"name": "End", "type": "int", "help": "The end position", "required": True, "input": "number",
                "default": 0},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.start = int(arguments["start"])
        self.end = int(arguments["end"])
        self.output = arguments["output"]

    def __call__(self, row):
        try:
            row[self.output] = row[self.field][self.start:self.end]
        except:
            row[self.output] = ""

        return row


