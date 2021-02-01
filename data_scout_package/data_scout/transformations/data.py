import math
import numpy as np
import pandas as pd
from datetime import datetime

from ._utils import get_param_int
from .statistics import StatsBase
from .transformation import Transformation


class Convert(Transformation):
    title = "Convert {field} to {to}"
    key = "Convert"
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
        super().__init__(arguments, sample_size, example)
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
    key = "Convert to datetime"
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
        super().__init__(arguments, sample_size, example)
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
    key = "List/dict to columns"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The field to convert", "required": True,
                  "input": "column", "multiple": False, "default": "", "column_type": ["list", "dict"]},
        "prefix": {"name": "Prefix", "type": "string", "help": "The prefix before the column number.", "required": True,
                   "input": "text", "default": ""}
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.prefix = arguments["prefix"]

    def __call__(self, row, index: int):
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
    key = "Duplicate column"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to duplicate", "required": True,
                  "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output", "type": "string", "help": "The name of the new column.", "required": True,
                   "input": "text", "default": ""}
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        if self.field in row:
            row[self.output] = row[self.field]

        return row, index


class DropColumn(Transformation):
    title = "Drop {field}"
    key = "Drop column"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The field to convert", "required": True,
                  "input": "column", "multiple": False, "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]

    def __call__(self, row, index: int):
        del row[self.field]
        return row, index


class RenameColumn(Transformation):
    title = "Rename {field} to {new}"
    key = "Rename column"
    fields = {
        "field": {"name": "Column", "type": "string", "help": "The column to rename", "required": True,
                  "input": "column", "multiple": False, "default": ""},
        "new": {"name": "New name", "type": "string", "help": "The new name of the column", "required": True,
                "input": "text", "multiple": False, "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.new = arguments["new"]

    def __call__(self, row, index: int):
        row[self.new] = row.pop(self.field)
        return row, index


class Transpose(Transformation):
    is_global = True
    title = "Transpose index and columns"
    key = "Transpose"
    fields = {
        "fields": StatsBase.fields["fields"],
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        self.fields = arguments["fields"]

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]
        rows = rows.transpose()
        return rows.reset_index().to_dict(orient="records"), index


class Shift(Transformation):
    is_global = True
    title = "Shift the values in {fields} by {periods}"
    key = "Shift column"
    fields = {
        "fields": StatsBase.fields["fields"],
        "periods": {"name": "Periods", "type": "number", "input": "number", "required": True,
                    "help": "The number of rows to shift the values (positive or negative)", "default": 1},
        "fill_value": {"name": "Fill value", "type": "number", "input": "number", "required": False,
                       "help": "Value to use when a value is missing", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.periods = get_param_int(arguments["periods"], 1)
        self.fill_value = get_param_int(arguments["fill_value"], None)

    def __call__(self, rows: pd.DataFrame, index: int):
        rows[self.fields] = rows[self.fields].shift(periods=self.periods, fill_value=self.fill_value)
        return rows.to_dict(orient="records"), index


class Diff(Transformation):
    is_global = True
    title = "Calculate the difference between values in {fields} (vertically)"
    key = "Differences in column (diff)"
    fields = {
        "fields": StatsBase.fields["fields"],
        "periods": Shift.fields["periods"],
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.periods = get_param_int(arguments["periods"], 1)

    def __call__(self, rows: pd.DataFrame, index: int):
        rows[self.fields] = rows[self.fields].diff(periods=self.periods)
        return rows.to_dict(orient="records"), index


class PctChange(Transformation):
    is_global = True
    title = "Calculate the percentual difference between values in {fields} (vertically)"
    key = "Percentual change in column (pctchange)"
    fields = {
        "fields": StatsBase.fields["fields"],
        "periods": Shift.fields["periods"],
        "fill_method": {"name": "Fill NA method", "type": "string", "required": True, "input": "select",
                        "multiple": False, "help": "How to handle NAs before computing percent changes",
                        "default": "pad", "options": {"bfill": "Backward fill", "ffill": "Forward fill", "": "None"}},
        "limit": {"name": "Limit", "type": "number", "input": "number", "required": False, "default": "",
                  "help": "The maximum number of consecutive NAs to fill before stopping (empty for no limit)."},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.periods = get_param_int(arguments["periods"], 1)
        self.fill_method = arguments["fill_method"] if arguments["fill_method"] != "" else None
        self.limit = get_param_int(arguments["limit"], None)

    def __call__(self, rows: pd.DataFrame, index: int):
        rows[self.fields] = rows[self.fields].pct_change(periods=self.periods, fill_method=self.fill_method,
                                                         limit=self.limit)
        return rows.to_dict(orient="records"), index


class CleanJSON:
    """
    This transformation cleans to object to present valid JSON. It's NOT meant to be used by the user. This is only for
    internal usage.
    """
    def __call__(self, row, index: int):
        for key, value in row.items():
            if value is math.nan or (isinstance(value, float) and np.isnan(value)):
                row[key] = "NaN"

        return row, index


class GetFields:

    def __init__(self):
        pass

    def spark(self, records):
        return records.flatMap(lambda x: x.keys()).distinct().collect()

    def __call__(self, records, index: int):
        pass


class MissingColumns(Transformation):
    """
    Add missing columns to the rows. Only for internal use.
    """
    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.columns = arguments["columns"]

    def __call__(self, row, index: int):
        for key in self.columns:
            if key not in row.keys():
                row[key] = None
        return row

