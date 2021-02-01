import re
from text_unidecode import unidecode

from .transformation import Transformation


class Format(Transformation):
    fields = {
        "fields": {"name": "Columns", "type": "list<string>", "help": "The fields to re-format",
                   "required": True, "input": "column", "multiple": True, "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        """Initialize the transformation with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]

    def __call__(self, row, index: int):
        raise NotImplementedError


class UpperCase(Format):
    title = "Convert {fields} to uppercase"
    key = "To uppercase"

    def __call__(self, row, index: int):
        for field in [f for f in self.fields if f in row]:
            row[field] = row[field].upper()

        return row, index


class LowerCase(Format):
    title = "Convert {fields} to lowercase"
    key = "To lowercase"

    def __call__(self, row, index: int):
        for field in [f for f in self.fields if f in row]:
            row[field] = row[field].lower()

        return row, index


class ProperCase(Format):
    title = "Convert {fields} to proper case"
    key = "To propercase"

    def __call__(self, row, index: int):
        for field in [f for f in self.fields if f in row]:
            row[field] = row[field].title()

        return row, index


class Trim(Transformation):
    character = None
    key = "Trim"
    fields = {
        "fields": {"name": "Columns", "type": "list<string>", "help": "The fields to trim",
                   "required": True, "input": "column", "multiple": True, "default": ""},
        "side": {"name": "Side", "type": "string", "help": "Which side of the string should be trimmed?",
                 "required": True, "input": "select", "multiple": False, "default": "",
                 "options": {"both": "Both", "left": "Left", "right": "Right"}}
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.side = arguments["side"]

    def __call__(self, row, index: int):
        if self.side == "left":
            for field in [f for f in self.fields if f in row]:
                row[field] = row[field].lstrip(self.character)
        elif self.side == "right":
            for field in [f for f in self.fields if f in row]:
                row[field] = row[field].rstrip(self.character)
        elif self.side == "both":
            for field in [f for f in self.fields if f in row]:
                row[field] = row[field].strip(self.character)

        return row, index


class TrimWhitespace (Trim):
    title = "Trim {fields} of whitespace"
    key = "Trim whitespace"
    character = None


class TrimQuotes(Trim):
    title = "Trim {fields} of quotes"
    key = "Trim quotes"
    character = "'\""


class RemoveWhitespace(Format):
    title = "Remove whitespace from {fields}"
    key = "Remove whitespace"

    def __call__(self, row, index: int):
        pattern = re.compile(r'\s+')
        for field in [f for f in self.fields if f in row]:
            row[field] = pattern.sub('', row[field])

        return row, index


class RemoveQuotes(Format):
    title = "Remove quotes from {fields}"
    key = "Remove quotes"

    def __call__(self, row, index: int):
        for field in [f for f in self.fields if f in row]:
            row[field] = row[field].replace("'", "").replace('"', "")

        return row, index


class RemoveSymbols(Format):
    title = "Remove symbols from {fields}"
    key = "Remove symbols"

    def __call__(self, row, index: int):
        pattern = re.compile(r'[\W_]+')
        for field in [f for f in self.fields if f in row]:
            row[field] = pattern.sub('', row[field])

        return row, index


class RemoveAccents(Format):
    title = "Remove accents from {fields}"
    key = "Remove accents"

    def __call__(self, row, index: int):
        for field in [f for f in self.fields if f in row]:
            row[field] = unidecode(row[field])

        return row, index


class AddFix(Transformation):
    fields = {
        "fields": {"name": "Columns", "type": "list<string>", "help": "The fields to trim",
                   "required": True, "input": "column", "multiple": True, "default": ""},
        "text": {"name": "Text", "type": "string", "help": "The text to add",
                 "required": True, "input": "text", "default": ""}
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.text = arguments["text"]

    def __call__(self, row, index: int):
        raise NotImplementedError


class AddPrefix(AddFix):
    title = "Add the prefix {text} to {fields}"
    key = "Add prefix"

    def __call__(self, row, index: int):
        for field in [f for f in self.fields if f in row]:
            row[field] = self.text + row[field]

        return row, index


class AddSuffix(AddFix):
    title = "Add the suffix {text} to {fields}"
    key = "Add suffix"

    def __call__(self, row, index: int):
        for field in [f for f in self.fields if f in row]:
            row[field] = row[field] + self.text

        return row, index


class Pad(Transformation):
    title = "Pad {fields} {side} to {length} characters with {character}"
    key = "Pad"
    fields = {
        "fields": {"name": "Columns", "type": "list<string>", "help": "The fields to trim",
                   "required": True, "input": "column", "multiple": True, "default": ""},
        "character": {"name": "Character", "type": "string", "help": "The character to pad the string with",
                      "required": True, "input": "text", "default": ""},
        "length": {"name": "Length", "type": "number", "help": "What should be the length of the resulting string",
                   "required": True, "input": "number", "default": 0},
        "side": {"name": "Side", "type": "string", "help": "On which side should the padding take place",
                 "required": True, "input": "select", "multiple": False, "default": "",
                 "options": {"left": "Left", "right": "Right"}}
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.character = arguments["character"]
        self.length = arguments["length"]
        self.side = arguments["side"]

    def __call__(self, row, index: int):
        if self.side == "left":
            for field in [f for f in self.fields if f in row]:
                row[field] = row[field].rjust(self.length, self.character)
        else:
            for field in [f for f in self.fields if f in row]:
                row[field] = row[field].ljust(self.length, self.character)

        return row, index


class Number(Transformation):
    title = "Format {fields} as numbers"
    key = "Format as number"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to format",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "decimals": {"name": "Length", "type": "number", "help": "What should be the length of the resulting string",
                     "required": True, "input": "number", "default": 0},
        "decimal_sep": {"name": "Decimal separator", "type": "string", "required": True, "input": "text",
                        "help": "The character to use as the decimal separator", "default": ""},
        "thousands_sep": {"name": "Thousands separator", "type": "string", "required": True, "input": "text",
                          "help": "The character to use as the thousands separator", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.decimals = int(arguments["decimals"])
        self.decimal_sep = str(arguments["decimal_sep"])
        self.thousands_sep = str(arguments["thousands_sep"])
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = ("{:,." + str(self.decimals) + "f}")\
            .format(row[self.field])\
            .replace(",", "THOUSANDS_SEP")\
            .replace(".", "DECIMAL_SEP")\
            .replace("DECIMAL_SEP", self.decimal_sep)\
            .replace("THOUSANDS_SEP", self.thousands_sep)

        return row, index
