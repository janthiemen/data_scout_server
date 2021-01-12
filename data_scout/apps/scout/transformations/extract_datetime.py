import math
from datetime import datetime
from apps.scout.transformations.transformation import Transformation


class ExtractBasic(Transformation):

    title = "Extract year from {field} into {output}"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        pass


class ExtractYear(ExtractBasic):
    title = "Extract year from {field} into {output}"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].year
        return row, index


class ExtractMonth(ExtractBasic):
    title = "Extract month from {field} into {output}"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].month
        return row, index


class ExtractDay(ExtractBasic):
    title = "Extract day from {field} into {output}"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].day
        return row, index


class ExtractWeek(ExtractBasic):
    title = "Extract week number from {field} into {output}"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].isocalendar()[1]
        return row, index


class ExtractDayOfWeek(ExtractBasic):
    title = "Extract the day of the week from {field} into {output} (Monday is 0)"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].weekday()
        return row, index


class ExtractDayOfYear(ExtractBasic):
    title = "Extract the day of the year from {field} into {output}"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].timetuple().tm_yday
        return row, index


class ExtractHours(ExtractBasic):
    title = "Extract the hours from {field} into {output}"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].hour
        return row, index


class ExtractMinutes(ExtractBasic):
    title = "Extract the minutes from {field} into {output}"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].minute
        return row, index


class ExtractSeconds(ExtractBasic):
    title = "Extract the seconds from {field} into {output}"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].second
        return row, index


class ExtractTimestamp(ExtractBasic):
    title = "Extract the timestamp from {field} into {output}"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = datetime.timestamp(row[self.field])
        return row, index
