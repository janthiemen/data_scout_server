import re
from text_unidecode import unidecode

from apps.scout.transformations.transformation import Transformation


class Format(Transformation):
    fields = {
        "fields": {"name": "Columns", "type": "list<string>", "help": "The fields to re-format",
                   "required": True, "input": "column", "multiple": True, "default": ""},
    }

    def __init__(self, arguments):
        """Initialize the transformation with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        self.fields = arguments["fields"]

    def __call__(self, row):
        raise NotImplementedError


class UpperCase(Format):
    title = "Convert {fields} to uppercase"

    def __call__(self, row):
        for field in self.fields:
            row[field] = row[field].upper()

        return row


class LowerCase(Format):
    title = "Convert {fields} to lowercase"

    def __call__(self, row):
        for field in self.fields:
            row[field] = row[field].lower()

        return row


class ProperCase(Format):
    title = "Convert {fields} to lowercase"

    def __call__(self, row):
        for field in self.fields:
            row[field] = row[field].title()

        return row


class Trim(Transformation):
    character = None
    fields = {
        "fields": {"name": "Columns", "type": "list<string>", "help": "The fields to trim",
                   "required": True, "input": "column", "multiple": True, "default": ""},
        "side": {"name": "Side", "type": "string", "help": "Which side of the string should be trimmed?",
                 "required": True, "input": "select", "multiple": False, "default": "",
                 "options": {"both": "Both", "left": "Left", "right": "Right"}}
    }

    def __init__(self, arguments):
        self.fields = arguments["fields"]
        self.side = arguments["side"]

    def __call__(self, row):
        if self.side == "left":
            for field in self.fields:
                row[field] = row[field].lstrip(self.character)
        elif self.side == "right":
            for field in self.fields:
                row[field] = row[field].rstrip(self.character)
        elif self.side == "both":
            for field in self.fields:
                row[field] = row[field].strip(self.character)

        return row


class TrimWhitespace (Trim):
    title = "Trim {fields} of whitespace"
    character = None


class TrimQuotes(Trim):
    title = "Trim {fields} of quotes"
    character = "'\""


class RemoveWhitespace(Format):
    title = "Remove whitespace from {fields}"

    def __call__(self, row):
        pattern = re.compile(r'\s+')
        for field in self.fields:
            row[field] = pattern.sub('', row[field])

        return row


class RemoveQuotes(Format):
    title = "Remove quotes from {fields}"

    def __call__(self, row):
        for field in self.fields:
            row[field] = row[field].replace("'", "").replace('"', "")

        return row


class RemoveSymbols(Format):
    title = "Remove symbols from {fields}"

    def __call__(self, row):
        pattern = re.compile(r'[\W_]+')
        for field in self.fields:
            row[field] = pattern.sub('', row[field])

        return row


class RemoveAccents(Format):
    title = "Remove accents from {fields}"

    def __call__(self, row):
        for field in self.fields:
            row[field] = unidecode(row[field])

        return row


class AddFix(Transformation):
    fields = {
        "fields": {"name": "Columns", "type": "list<string>", "help": "The fields to trim",
                   "required": True, "input": "column", "multiple": True, "default": ""},
        "text": {"name": "Text", "type": "string", "help": "The text to add",
                 "required": True, "input": "text", "default": ""}
    }

    def __init__(self, arguments):
        self.fields = arguments["fields"]
        self.text = arguments["text"]

    def __call__(self, row):
        raise NotImplementedError


class AddPrefix(AddFix):
    title = "Add the prefix {text} to {fields}"

    def __call__(self, row):
        for field in self.fields:
            row[field] = self.text + row[field]

        return row


class AddSuffix(AddFix):
    title = "Add the suffix {text} to {fields}"

    def __call__(self, row):
        for field in self.fields:
            row[field] = row[field] + self.text

        return row


class Pad(Transformation):
    title = "Pad {fields} {side} to {length} characters with {character}"
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

    def __init__(self, arguments):
        self.fields = arguments["fields"]
        self.character = arguments["character"]
        self.length = arguments["length"]
        self.side = arguments["side"]

    def __call__(self, row):
        if self.side == "left":
            for field in self.fields:
                row[field] = row[field].rjust(self.length, self.character)
        else:
            for field in self.fields:
                row[field] = row[field].ljust(self.length, self.character)

        return row
