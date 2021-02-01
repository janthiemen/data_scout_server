from ._utils import get_param_bool, get_param_int
from .transformation import Transformation
import pandas as pd
import numpy as np


class GroupByBase(Transformation):
    key = "Group by"
    fields = {
        "fields": {"name": "Fields", "type": "list<string>", "help": "The fields to check",
                   "required": True, "input": "column", "multiple": True, "default": []},
        "aggs": {"name": "Aggregations", "type": "list<agg>", "help": "The aggregations to make",
                 "required": True, "input": "multiple", "multiple": True, "default": [],
                 "sub_fields": {
                     "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                               "required": True, "input": "column", "multiple": False, "default": ""},
                     "agg": {"name": "Aggregation", "type": "string", "help": "",
                             "required": True, "input": "select", "multiple": False, "default": "",
                             "options": {"all": "All", "any": "Any", "bfill": "Backward fill", "ffill": "Forward fill",
                                         "count": "Count", "nunique": "Count distinct", "first": "First",
                                         "last": "Last", "nth": "Nth row", "max": "Max", "min": "Min", "mean": "Mean",
                                         "median": "Median", "sum": "Sum", "prod": "Product", "size": "Size",
                                         "sem": "Standard Error of the Mean", "std": "Standard deviation",
                                         "var": "Variance", "percentile": "Percentile", "list": "List",
                                         "unique": "Unique"}
                             },
                     "skipna": {"name": "Skip NA", "type": "string", "help": "Skip missing values?", "required": False,
                                "input": "select", "multiple": False, "default": "1",
                                "optional": {"agg": ["all", "any", "nunique", "nth"]},
                                "options": {"1": "Yes", "0": "No"}},
                     "numeric_only": {"name": "Numeric only", "type": "string",
                                      "help": "Only include numeric data?",
                                      "required": False, "input": "select", "multiple": False, "default": "0",
                                      "optional": {"agg": ["max", "mean", "median", "min", "prod", "sum"]},
                                      "options": {"1": "Yes", "0": "No"}},
                     "n": {"name": "Row index", "type": "number", "input": "number",
                           "help": "The zero-based row number of the row you want to select",
                           "required": False, "default": 0, "optional": {"agg": ["nth"]}},
                     "q": {"name": "Percentile", "type": "number", "input": "number",
                           "help": "The percentile to compute (between 0 and 100, inclusive)",
                           "required": False, "default": 0, "optional": {"agg": ["percentile"]}},
                     "min_count": {"name": "Minimum valid values", "type": "number", "input": "number",
                                   "help": "The minimum number of valid values in the group to computate the value. "
                                           "If it's not reached the result is NA.",
                                   "required": False, "default": "",
                                   "optional": {"agg": ["first", "last", "prod", "sum"]}},
                     "limit": {"name": "Limit", "type": "number", "help": "Limit of how many values to fill",
                               "required": False, "input": "number", "default": "",
                               "optional": {"agg": ["bfill", "ffill"]}},
                     "ddof": {"name": "Delta Degrees of freedom", "type": "number", "required": False,
                              "help": "Delta Degrees of Freedom. The divisor used in calculations is N - ddof, where N "
                                      "represents the number of elements.",
                              "input": "number", "default": "", "optional": {"agg": ["sem", "std", "var"]}},
                     "name": {"name": "Name", "type": "string", "help": "The name of the newly created column",
                              "required": True, "input": "text", "multiple": False, "default": ""},

                 }},
    }

    def _add_aggregation(self, name, field, function):
        self.aggregations[name] = (field, function)

    def _create_aggregations(self, aggs):
        for agg in aggs:
            agg["name"] = agg["name"].replace(" ", "_")
            if agg["agg"] == "all":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.all(skipna=get_param_bool(agg["skipna"])))
            elif agg["agg"] == "any":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.any(skipna=get_param_bool(agg["skipna"])))
            elif agg["agg"] == "bfill":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.bfill(
                    limit=get_param_int(agg["limit"], None)))
            elif agg["agg"] == "ffill":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.ffill(
                    limit=get_param_int(agg["limit"], None)))
            elif agg["agg"] == "count":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.count())
            elif agg["agg"] == "nunique":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.nunique(
                    dropna=get_param_bool(agg["skipna"])))
            elif agg["agg"] == "first":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.first())
            elif agg["agg"] == "last":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.last())
            elif agg["agg"] == "nth":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.iloc[get_param_int(agg["n"], 0)])
            elif agg["agg"] == "min":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.min(
                    numeric_only=get_param_bool(agg["numeric_only"])))
            elif agg["agg"] == "max":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.max(
                    numeric_only=get_param_bool(agg["numeric_only"])))
            elif agg["agg"] == "mean":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.mean(
                    numeric_only=get_param_bool(agg["numeric_only"])))
            elif agg["agg"] == "median":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.median(
                    numeric_only=get_param_bool(agg["numeric_only"])
                ))
            elif agg["agg"] == "percentile":
                self._add_aggregation(agg["name"], agg["field"], lambda x: np.percentile(x, get_param_int(agg["q"], 0)))
            elif agg["agg"] == "sum":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.sum(
                    numeric_only=get_param_bool(agg["numeric_only"])
                ))
            elif agg["agg"] == "prod":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.prod(
                    numeric_only=get_param_bool(agg["numeric_only"]), min_count=get_param_int(agg["min_count"], -1)))
            elif agg["agg"] == "size":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.size)
            elif agg["agg"] == "sem":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.sem(ddof=get_param_int(agg["ddof"], 1)))
            elif agg["agg"] == "std":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.std(ddof=get_param_int(agg["ddof"], 1)))
            elif agg["agg"] == "var":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.var(ddof=get_param_int(agg["ddof"], 1)))
            elif agg["agg"] == "list":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.tolist())
            elif agg["agg"] == "unique":
                self._add_aggregation(agg["name"], agg["field"], lambda x: x.unique().tolist())
        # TODO: Add percentual change, diff, shift

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.aggregations = {}
        self._create_aggregations(arguments["aggs"])

    def __call__(self, row, index: int):
        raise NotImplemented


class GroupBy(GroupByBase):
    is_global = True
    title = "Group the data by {fields}"
    fields = {
        "fields": {"name": "Fields", "type": "list<string>", "help": "The fields to check",
                   "required": True, "input": "column", "multiple": True, "default": []},
        "aggs": GroupByBase.fields["aggs"]
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]

    def __call__(self, rows: pd.DataFrame, index: int):
        # TODO: Check if something breaks when there's a column name containing numbers
        # TODO: Check if all these transforms are possible in Spark
        return rows.groupby(self.fields)\
                   .agg(**self.aggregations)\
                   .reset_index()\
                   .to_dict(orient="records"), \
               index



    """
    Group by's that return the same number of rows as the original set (i.e. aren't compatible with the others):
        GroupBy.cumcount([ascending])
        GroupBy.cummax([axis])
        GroupBy.cummin([axis])
        GroupBy.cumprod([axis])
        GroupBy.cumsum([axis])
        GroupBy.head([n])
        GroupBy.tail([n])
        GroupBy.ngroup([ascending])
        GroupBy.rank([method, ascending, na_option, …])
        GroupBy.pct_change([periods, fill_method, …])
    """
