import math
import numpy as np
from datetime import datetime

from apps.scout.transformations.transformation import Transformation


class Convert(Transformation):
    title = "Convert {field} to {to}"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The field to convert", "required": True,
                  "input": "column", "multiple": False, "default": ""},
        "to": {"name": "To", "type": "string", "help": "To which data type to convert", "required": True,
               "input": "select", "multiple": False, "default": "",
               "options": {"int": "Integer", "float": "Floating point number", "string": "Text", "bool": "Boolean"}}
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        """Initialize the transformation with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        self.field = arguments["field"]
        self.to = arguments["to"]

    def __call__(self, row, index: int):
        """This class is called on each row.

        Arguments:
            row {dict} -- The complete row

        Returns:
            dict -- The row, including the extra output column
        """
        if self.field not in row:
            return row, index

        try:
            if self.to == "int":
                row[self.field] = int(row[self.field])
            elif self.to == "bool":
                row[self.field] = bool(row[self.field])
            elif self.to == "string":
                row[self.field] = str(row[self.field])
            elif self.to == "float" or self.to == 'Floating point number':
                row[self.field] = float(row[self.field])
        except ValueError as e:
            row[self.field] = math.nan
        return row, index


class ConvertDatetime(Transformation):
    title = "Convert {field} to datetime"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The field to convert", "required": True,
                  "input": "column", "multiple": False, "default": ""},
        "format": {"name": "Format", "type": "string",
                   "help": "The datatime format of the input (according to the Python datetime format codes https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).", "required": True,
                   "input": "text", "default": "%Y-%m-%d %H:%M"}
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        """Initialize the transformation with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        self.field = arguments["field"]
        self.format = arguments["format"]

    def __call__(self, row, index: int):
        """This class is called on each row.

        Arguments:
            row {dict} -- The complete row

        Returns:
            dict -- The row, including the extra output column
        """
        if self.field not in row:
            return row, index
        row[self.field] = datetime.strptime(row[self.field], self.format)
        return row, index


class FieldToColumn(Transformation):
    title = "Convert {field} to columns"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The field to convert", "required": True,
                  "input": "column", "multiple": False, "default": "", "column_type": ["list", "dict"]},
        "prefix": {"name": "Prefix", "type": "string", "help": "The prefix before the column number.", "required": True,
                   "input": "text", "default": ""}
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        """Initialize the transformation with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        self.field = arguments["field"]
        self.prefix = arguments["prefix"]

    def __call__(self, row, index: int):
        """This class is called on each row.

        Arguments:
            row {dict} -- The complete row

        Returns:
            dict -- The row, including the extra output column
        """
        if self.field not in row:
            return row, index

        if isinstance(row[self.field], list):
            for i, val in enumerate(row[self.field]):
                row[f"{self.prefix}-{i}"] = val
            del row[self.field]
        elif isinstance(row[self.field], dict):
            for key, val in row[self.field].items():
                row[f"{self.prefix}-{key}"] = val
            del row[self.field]

        return row, index


class DuplicateColumn(Transformation):
    title = "Duplicate {field} as {output}"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to duplicate", "required": True,
                  "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output", "type": "string", "help": "The name of the new column.", "required": True,
                   "input": "text", "default": ""}
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        if self.field in row:
            row[self.output] = row[self.field]

        return row, index


class DropColumn(Transformation):
    title = "Drop {field}"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The field to convert", "required": True,
                  "input": "column", "multiple": False, "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        self.field = arguments["field"]

    def __call__(self, row, index: int):
        del row[self.field]
        return row, index


class CleanJSON:
    """
    This transformation cleans to object to present valid JSON. It's NOT meant to be used by the user. This is only for
    internal usage.
    """
    def __call__(self, row, index: int):
        """This class is called on each row.

        Arguments:
            row {dict} -- The complete row

        Returns:
            dict -- The row, including the extra output column
        """
        for key, value in row.items():
            if value is math.nan or (isinstance(value, float) and np.isnan(value)):
                row[key] = "NaN"

        return row, index
