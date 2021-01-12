import math
import re
import urllib.parse as urlparse
from urllib.parse import parse_qs

from apps.scout.transformations.transformation import Transformation


class ExtractBasic(Transformation):

    title = "Extract year from {field} into {output}"
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
        pass


class ExtractYear(ExtractBasic):
    title = "Extract year from {field} into {output}"

    def __call__(self, row):
        row[self.output] = row[self.field].year
        return row


class ExtractMonth(ExtractBasic):
    title = "Extract month from {field} into {output}"

    def __call__(self, row):
        row[self.output] = row[self.field].month
        return row


class ExtractDay(ExtractBasic):
    title = "Extract day from {field} into {output}"

    def __call__(self, row):
        row[self.output] = row[self.field].day
        return row


class ExtractWeek(ExtractBasic):
    title = "Extract week number from {field} into {output}"

    def __call__(self, row):
        row[self.output] = row[self.field].isocalendar()[1]
        return row


class ExtractDayOfWeek(ExtractBasic):
    title = "Extract the day of the week from {field} into {output} (Monday is 0)"

    def __call__(self, row):
        row[self.output] = row[self.field].weekday()
        return row


class ExtractDayOfYear(ExtractBasic):
    title = "Extract the day of the year from {field} into {output}"

    def __call__(self, row):
        row[self.output] = row[self.field].timetuple().tm_yday
        return row


class ExtractHours(ExtractBasic):
    title = "Extract the hours from {field} into {output}"

    def __call__(self, row):
        row[self.output] = row[self.field].hour
        return row


class ExtractMinutes(ExtractBasic):
    title = "Extract the minutes from {field} into {output}"

    def __call__(self, row):
        row[self.output] = row[self.field].minute
        return row


class ExtractSeconds(ExtractBasic):
    title = "Extract the seconds from {field} into {output}"

    def __call__(self, row):
        row[self.output] = row[self.field].second
        return row
