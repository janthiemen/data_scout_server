import math
from datetime import datetime, timedelta, date
import calendar
from .transformation import Transformation


class ExtractBasic(Transformation):

    title = "Extract year from {field} into {output}"
    key = "Datetime minutes"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input", "column_type": ["datetime"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        pass


class ExtractYear(ExtractBasic):
    title = "Extract year from {field} into {output}"
    key = "Datetime year"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].year
        return row, index


class ExtractMonth(ExtractBasic):
    title = "Extract month from {field} into {output}"
    key = "Datetime month"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].month
        return row, index


class ExtractMonthName(ExtractBasic):
    title = "Extract month name from {field} into {output}"
    key = "Datetime month name"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = ""
        else:
            row[self.output] = row[self.field].strftime('%B')
        return row, index


class ExtractEndOfMonth(ExtractBasic):
    title = "Get the last day of the month from {field} into {output}"
    key = "Datetime end of month"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = ""
        else:
            row[self.output] = calendar.monthrange(row[self.field].year, row[self.field].month)[1]
        return row, index


class ExtractDay(ExtractBasic):
    title = "Extract day from {field} into {output}"
    key = "Datetime day"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].day
        return row, index


class ExtractWeek(ExtractBasic):
    title = "Extract week number from {field} into {output}"
    key = "Datetime week"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].isocalendar()[1]
        return row, index


class ExtractDayOfWeek(ExtractBasic):
    title = "Extract the day of the week from {field} into {output} (Monday is 0)"
    key = "Datetime day of week"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].weekday()
        return row, index


class ExtractDayOfWeekName(ExtractBasic):
    title = "Extract the name of the day of the week from {field} into {output}"
    key = "Datetime day of week name"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = ""
        else:
            row[self.output] = row[self.field].strftime('%A')
        return row, index


class ExtractDayOfYear(ExtractBasic):
    title = "Extract the day of the year from {field} into {output}"
    key = "Datetime day of year"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].timetuple().tm_yday
        return row, index


class ExtractHours(ExtractBasic):
    title = "Extract the hours from {field} into {output}"
    key = "Datetime hours"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].hour
        return row, index


class ExtractMinutes(ExtractBasic):
    title = "Extract the minutes from {field} into {output}"
    key = "Datetime minutes"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].minute
        return row, index


class ExtractSeconds(ExtractBasic):
    title = "Extract the seconds from {field} into {output}"
    key = "Datetime seconds"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = row[self.field].second
        return row, index


class ExtractTimestamp(ExtractBasic):
    title = "Extract the timestamp from {field} into {output}"
    key = "Datetime timestamp"

    def __call__(self, row, index: int):
        if self.field not in row:
            row[self.output] = math.nan
        else:
            row[self.output] = datetime.timestamp(row[self.field])
        return row, index


class DateAdd(Transformation):
    title = "Move {field} by a certain amount of time"
    key = "Datetime add"
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input", "column_type": ["datetime"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "weeks": {"name": "Weeks", "type": "number", "help": "The weeks that should be added",
                  "required": True, "input": "number", "multiple": False, "default": 0},
        "days": {"name": "Days", "type": "number", "help": "The days that should be added",
                 "required": True, "input": "number", "multiple": False, "default": 0},
        "hours": {"name": "Hours", "type": "number", "help": "The hours that should be added",
                  "required": True, "input": "number", "multiple": False, "default": 0},
        "minutes": {"name": "Minutes", "type": "number", "help": "The minutes that should be added",
                    "required": True, "input": "number", "multiple": False, "default": 0},
        "seconds": {"name": "Seconds", "type": "number", "help": "The seconds that should be added",
                    "required": True, "input": "number", "multiple": False, "default": 0},
        "milliseconds": {"name": "Milliseconds", "type": "number", "help": "The milliseconds that should be added",
                         "required": True, "input": "number", "multiple": False, "default": 0},
        "microseconds": {"name": "Microseconds", "type": "number", "help": "The microseconds that should be added",
                         "required": True, "input": "number", "multiple": False, "default": 0},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.delta = timedelta(
            weeks=int(arguments["weeks"]),
            days=int(arguments["days"]),
            hours=int(arguments["hours"]),
            minutes=int(arguments["minutes"]),
            seconds=int(arguments["seconds"]),
            milliseconds=int(arguments["milliseconds"]),
            microseconds=int(arguments["microseconds"])
        )

        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = row[self.field] + self.delta
        return row, index


class DateDiff(Transformation):
    title = "Calculate {field_a} - {field_b} in {unit}"
    key = "Datetime difference"
    fields = {
        "field_a": {"name": "Date 1", "type": "string", "help": "The first date", "column_type": ["datetime"],
                    "required": True, "input": "column", "multiple": False, "default": ""},
        "field_b": {"name": "Date 2", "type": "string", "help": "The second date", "column_type": ["datetime"],
                    "required": True, "input": "column", "multiple": False, "default": ""},
        "unit": {"name": "Unit", "type": "string", "help": "The unit that should be calculated",
                 "required": True, "input": "select", "multiple": False, "default": "days",
                 "options": {"weeks": "weeks", "days": "days", "hours": "hours", "minutes": "minutes",
                             "seconds": "seconds", "milliseconds": "milliseconds", "microseconds": "microseconds"}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field_a = arguments["field_a"]
        self.field_b = arguments["field_b"]
        self.unit = arguments["unit"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        delta = self.field_a - self.field_b
        if self.unit == "weeks":
            row[self.output] = math.floor(delta.days / 7)
        elif self.unit == "days":
            row[self.output] = delta.days
        elif self.unit == "hours":
            row[self.output] = math.floor(delta.seconds / 3600)
        elif self.unit == "minutes":
            row[self.output] = math.floor(delta.seconds / 60)
        elif self.unit == "seconds":
            row[self.output] = delta.seconds
        elif self.unit == "milliseconds":
            row[self.output] = delta.seconds * 1000
        elif self.unit == "microseconds":
            row[self.output] = delta.seconds * 1000000

        return row, index


class Now(Transformation):
    title = "Current datetime into {output}"
    key = "Datetime now"
    fields = {
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        row[self.output] = datetime.now()
        return row, index


class Today(Transformation):
    title = "Current date into {output}"
    key = "Datetime today"
    fields = {
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        t = date.today()
        row[self.output] = datetime(t.year, t.month, t.day)
        return row, index
