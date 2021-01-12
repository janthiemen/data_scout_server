import math
import re

from apps.scout.transformations.transformation import Transformation


class ReplaceText(Transformation):
    title = "Replace exact matches of {old} with {new} in {field} as {output}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "old": {"name": "Search", "type": "string", "help": "The old substring you want to replace.",
                "required": True, "input": "text", "default": ""},
        "new": {"name": "New", "type": "string", "help": "The new substring which would replace the old substring",
                "required": True, "input": "text", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.old = arguments["old"]
        self.new = arguments["new"]
        self.output = arguments["output"]

    def __call__(self, row):
        row[self.output] = row[self.field].replace(self.old, self.new)

        return row


class ReplaceRegex(Transformation):
    title = "Replace matches of the regex {pattern} with {new} in {field} as {output}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "pattern": {"name": "Pattern", "type": "regex", "help": "The regex pattern that should be replaced",
                    "required": True, "input": "text", "default": ""},
        "new": {"name": "New", "type": "string", "help": "The new substring which would replace the old substring",
                "required": True, "input": "text", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.pattern = re.compile(arguments["pattern"])
        self.new = arguments["new"]
        self.output = arguments["output"]

    def __call__(self, row):
        # TODO: Check if the regex is correct
        row[self.output] = re.sub(self.pattern, self.new, row[self.field])

        return row


class ReplaceDelimiters(Transformation):
    title = "Replace all characters between the delimiter: {delimiter} in {field} as {output}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "delimiter": {"name": "Delimiter", "type": "string", "help": "The delimiter to split the string on",
                      "required": True, "input": "text", "default": ""},
        "new": {"name": "New", "type": "string", "help": "The new substring which would replace the old substring",
                "required": True, "input": "text", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.pattern = re.compile('{delimiter}.*{delimiter}'.format(delimiter=arguments["delimiter"]), flags=re.DOTALL)
        self.new = arguments["new"]
        self.output = arguments["output"]

    def __call__(self, row):
        # TODO: Check if the regex is correct
        row[self.output] = re.sub(self.pattern, self.new, row[self.field])
        return row


class ReplacePositions(Transformation):
    title = "Replace all characters between pos. {start} - {end} with {new} into {output}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "start": {"name": "Start", "type": "int", "help": "The start position", "required": True, "input": "number",
                  "default": 0},
        "end": {"name": "End", "type": "int", "help": "The end position", "required": True, "input": "number",
                "default": 0},
        "new": {"name": "New", "type": "string", "help": "The new substring which would replace the old substring",
                "required": True, "input": "text", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.start = arguments["start"]
        self.end = arguments["end"]
        self.new = arguments["new"]
        self.output = arguments["output"]

    def __call__(self, row):
        # TODO: Check if string is long enough and start < end
        row[self.output] = row[self.field][:self.start] + self.new + row[self.field][self.end:]
        return row


class ReplaceMismatched(Transformation):
    title = "Replace mismatched values in {field} with {new}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "new": {"name": "New", "type": "string", "help": "The new value", "required": True, "input": "text",
                "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.new = arguments["new"]

    def __call__(self, row):
        if row[self.field] is math.nan:
            row[self.field] = self.new
        return row


class ReplaceMissing(Transformation):
    title = "Replace missing values in {field} with {new}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "new": {"name": "New", "type": "string", "help": "The new value", "required": True, "input": "text",
                "default": ""},
    }

    def __init__(self, arguments: dict, example: dict = None):
        self.field = arguments["field"]
        self.new = arguments["new"]

    def __call__(self, row):
        if row[self.field] is None or len(row[self.field]) == 0:
            row[self.field] = self.new
        return row


