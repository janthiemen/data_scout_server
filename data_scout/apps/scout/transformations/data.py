import math
from datetime import datetime

from apps.scout.transformations.transformation import Transformation


class Convert(Transformation):
    title = "Convert {field} to {to}"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The field to convert", "required": True,
                  "input": "column", "multiple": False, "default": ""},
        "to": {"name": "To", "type": "string", "help": "To which data type to convert", "required": True,
               "input": "select", "multiple": False, "default": "",
               "options": {"int": "Integer", "float": "Floating point number", "string": "Text"}}
    }

    def __init__(self, arguments: dict, example: dict = None):
        """Initialize the transformation with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        self.field = arguments["field"]
        self.to = arguments["to"]

    def __call__(self, row):
        """This class is called on each row.

        Arguments:
            row {dict} -- The complete row

        Returns:
            dict -- The row, including the extra output column
        """
        try:
            if self.to == "int":
                row[self.field] = int(row[self.field])
            elif self.to == "float" or self.to == 'Floating point number':
                row[self.field] = float(row[self.field])
        except ValueError as e:
            row[self.field] = math.nan
        return row


class ConvertDatetime(Transformation):
    title = "Convert {field} to datetime"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The field to convert", "required": True,
                  "input": "column", "multiple": False, "default": ""},
        "format": {"name": "Format", "type": "string", "help": "The datatime format of the input (according to the Python datetime format codes https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).", "required": True,
                   "input": "text", "default": "%Y-%m-%d %H:%M"}
    }

    def __init__(self, arguments: dict, example: dict = None):
        """Initialize the transformation with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        self.field = arguments["field"]
        self.format = arguments["format"]

    def __call__(self, row):
        """This class is called on each row.

        Arguments:
            row {dict} -- The complete row

        Returns:
            dict -- The row, including the extra output column
        """
        row[self.field] = datetime.strptime(row[self.field], self.format)
        return row


class CleanJSON:
    """
    This transformation cleans to object to present valid JSON. It's NOT meant to be used by the user. This is only for
    internal usage.
    """
    def __call__(self, row):
        """This class is called on each row.

        Arguments:
            row {dict} -- The complete row

        Returns:
            dict -- The row, including the extra output column
        """
        for key, value in row.items():
            if value is math.nan:
                row[key] = "NaN"

        return row
