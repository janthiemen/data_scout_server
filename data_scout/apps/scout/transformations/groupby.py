from typing import List

from apps.scout.transformations._utils import get_param_bool, get_param_int
from apps.scout.transformations.transformation import Transformation
import pandas as pd


class GroupBy(Transformation):
    is_global = True
    title = "Group the data by {fields}"
    fields = {
        "fields": {"name": "Fields", "type": "list<string>", "help": "The fields to check",
                   "required": True, "input": "column", "multiple": True, "default": ""},
        "aggs": {"name": "Aggregations", "type": "list<agg>", "help": "The aggregations to make",
                 "required": True, "input": "multiple", "multiple": True, "default": "",
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
                                         "var": "Variance"}
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
                     "min_count": {"name": "Minimum valid values", "type": "number", "input": "number",
                                   "help": "The minimum number of valid values in the group to computate the value. "
                                           "If it's not reached the result is NA.",
                                   "required": False, "default": "",
                                   "optional": {"agg": ["first", "last", "prod", "sum"]}},
                     "limit": {"name": "Limit", "type": "number", "help": "Limit of how many values to fill",
                               "required": False, "input": "number", "default": "",
                               "optional": {"agg": ["bfill", "ffill"]}},
                     "ddof": {"name": "Degrees of freedom", "type": "number", "help": "The degrees of freedom",
                              "required": False, "input": "number", "default": "",
                              "optional": {"agg": ["sem", "std", "var"]}},
                     "name": {"name": "Name", "type": "string", "help": "The name of the newly created column",
                              "required": True, "input": "text", "multiple": False, "default": ""},

                 }},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        self.fields = arguments["fields"]
        self.aggregations = {}
        for agg in arguments["aggs"]:
            agg["name"] = agg["name"].replace(" ", "_")
            if agg["agg"] == "all":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.all(skipna=get_param_bool(agg["skipna"])))
            elif agg["agg"] == "any":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.any(skipna=get_param_bool(agg["skipna"])))
            elif agg["agg"] == "bfill":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.bfill(
                    limit=get_param_int(agg["limit"], None)))
            elif agg["agg"] == "ffill":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.ffill(
                    limit=get_param_int(agg["limit"], None)))
            elif agg["agg"] == "count":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.count())
            elif agg["agg"] == "nunique":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.nunique(
                    dropna=get_param_bool(agg["skipna"])))
            elif agg["agg"] == "first":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.first())
            elif agg["agg"] == "last":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.last())
            elif agg["agg"] == "nth":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.iloc[get_param_int(agg["n"], 0)])
            elif agg["agg"] == "min":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.min(
                    numeric_only=get_param_bool(agg["numeric_only"])))
            elif agg["agg"] == "max":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.max(
                    numeric_only=get_param_bool(agg["numeric_only"])))
            elif agg["agg"] == "mean":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.mean(
                    numeric_only=get_param_bool(agg["numeric_only"])))
            elif agg["agg"] == "median":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.median(
                    numeric_only=get_param_bool(agg["numeric_only"])
                ))
            elif agg["agg"] == "sum":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.sum(
                    numeric_only=get_param_bool(agg["numeric_only"])
                ))
            elif agg["agg"] == "prod":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.prod(
                    numeric_only=get_param_bool(agg["numeric_only"]), min_count=get_param_int(agg["min_count"], -1)))
            elif agg["agg"] == "size":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.size())
            elif agg["agg"] == "sem":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.sem(ddof=get_param_int(agg["ddof"], 1)))
            elif agg["agg"] == "std":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.std(ddof=get_param_int(agg["ddof"], 1)))
            elif agg["agg"] == "var":
                self.aggregations[agg["name"]] = (agg["field"], lambda x: x.var(ddof=get_param_int(agg["ddof"], 1)))

        # fields = {
        #     "fields": {"name": "Fields", "type": "list<string>", "help": "The fields to check",
        #                "required": True, "input": "column", "multiple": True, "default": ""},
        #     "aggs": {"name": "Aggregations", "type": "list<agg>", "help": "The aggregations to make",
        #              "required": True, "input": "multiple", "multiple": True, "default": "",
        #              "sub_fields": {
        #                  "field": {"name": "Input", "type": "string", "help": "The column to use as input",
        #                            "required": True, "input": "column", "multiple": False, "default": ""},
        #                  "agg": {"name": "Aggregation", "type": "string", "help": "",
        #                          "required": True, "input": "select", "multiple": False, "default": "",
        #                          "options": {"all": "All", "any": "Any", "bfill": "Backward fill",
        #                                      "ffill": "Forward fill",
        #                                      "count": "Count", "nunique": "Count distinct", "first": "First",
        #                                      "last": "Last", "nth": "Nth row", "max": "Max", "min": "Min",
        #                                      "mean": "Mean",
        #                                      "median": "Median", "sum": "Sum", "prod": "Product", "size": "Size",
        #                                      "sem": "Standard Error of the Mean", "std": "Standard deviation",
        #                                      "var": "Variance", "ohlc": "Open, High, Low, Close"}
        #                          },
        #                  "skipna": {"name": "Skip NA", "type": "string", "help": "Skip missing values?",
        #                             "required": False,
        #                             "input": "select", "multiple": False, "default": "1",
        #                             "optional": {"agg": ["all", "any", "nunique", "nth"]},
        #                             "options": {"1": "Yes", "0": "No"}},
        #                  "numeric_only": {"name": "Numeric only", "type": "string",
        #                                   "help": "Only include numeric data?",
        #                                   "required": False, "input": "select", "multiple": False, "default": "0",
        #                                   "optional": {"agg": ["first", "last", "max", "mean", "median", "min", "prod",
        #                                                        "sum"]},
        #                                   "options": {"1": "Yes", "0": "No"}},
        #                  "n": {"name": "Row index", "type": "number", "input": "number",
        #                        "help": "The zero-based row number of the row you want to select",
        #                        "required": False, "default": 0, "optional": {"agg": ["nth"]}},
        #                  "min_count": {"name": "Minimum valid values", "type": "number", "input": "number",
        #                                "help": "The minimum number of valid values in the group to computate the value. "
        #                                        "If it's not reached the result is NA.",
        #                                "required": False, "default": "",
        #                                "optional": {"agg": ["first", "last", "max", "min", "prod", "sum"]}},
        #                  "limit": {"name": "Limit", "type": "number", "help": "Limit of how many values to fill",
        #                            "required": False, "input": "number", "default": "",
        #                            "optional": {"agg": ["bfill", "ffill"]}},
        #                  "ddof": {"name": "Degrees of freedom", "type": "number", "help": "The degrees of freedom",
        #                           "required": False, "input": "number", "default": "",
        #                           "optional": {"agg": ["sem", "std", "var"]}},
        #                  "name": {"name": "Name", "type": "string", "help": "The name of the newly created column",
        #                           "required": True, "input": "text", "multiple": False, "default": ""},
        #
        #              }},
        # }

        # for agg in arguments["aggs"]:
        #     if agg["agg"] == "all":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.all(skipna=get_param_bool(agg["skipna"])))
        #     elif agg["agg"] == "any":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.any(skipna=get_param_bool(agg["skipna"])))
        #     elif agg["agg"] == "bfill":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.bfill(
        #             limit=get_param_int(agg["limit"], None)))
        #     elif agg["agg"] == "ffill":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.ffill(
        #             limit=get_param_int(agg["limit"], None)))
        #     elif agg["agg"] == "count":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.count())
        #     elif agg["agg"] == "nunique":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.nunique(
        #             skipna=get_param_bool(agg["skipna"])))
        #     elif agg["agg"] == "first":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.first(
        #             numeric_only=get_param_bool(agg["numeric_only"]), min_count=get_param_int(agg["min_count"], -1)))
        #     elif agg["agg"] == "last":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.last(
        #             numeric_only=get_param_bool(agg["numeric_only"]), min_count=get_param_int(agg["min_count"], -1)))
        #     elif agg["agg"] == "nth":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.nth(
        #             dropna=None if agg["skipna"] == "0" else "all", n=get_param_int(agg["n"], 0)))
        #     elif agg["agg"] == "min":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.min(
        #             numeric_only=get_param_bool(agg["numeric_only"]), min_count=get_param_int(agg["min_count"], -1)))
        #     elif agg["agg"] == "max":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.max(
        #             numeric_only=get_param_bool(agg["numeric_only"]), min_count=get_param_int(agg["min_count"], -1)))
        #     elif agg["agg"] == "mean":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.mean(
        #             numeric_only=get_param_bool(agg["numeric_only"])))
        #     elif agg["agg"] == "median":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.median(
        #             numeric_only=get_param_bool(agg["numeric_only"])))
        #     elif agg["agg"] == "sum":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.sum)
        #             # numeric_only=get_param_bool(agg["numeric_only"]), min_count=get_param_int(agg["min_count"], -1)))
        #     elif agg["agg"] == "prod":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.prod(
        #             numeric_only=get_param_bool(agg["numeric_only"]), min_count=get_param_int(agg["min_count"], -1)))
        #     elif agg["agg"] == "size":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.size())
        #     elif agg["agg"] == "sem":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.sem(ddof=get_param_int(agg["ddof"], 1)))
        #     elif agg["agg"] == "std":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.std(ddof=get_param_int(agg["ddof"], 1)))
        #     elif agg["agg"] == "var":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.var(ddof=get_param_int(agg["ddof"], 1)))
        #     elif agg["agg"] == "ohlc":
        #         self.aggregations[agg["name"]] = (agg["field"], lambda x: x.ohlc())

    def __call__(self, rows: List[dict], index: int):
        # TODO: Check if something breaks when there's a column name containing numbers
        # TODO: Check if all these transforms are possible in Spark
        return pd.DataFrame(rows)\
                   .groupby(self.fields)\
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
