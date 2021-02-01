from ._utils import get_param_int
from .transformation import Transformation
import pandas as pd


class StatsBase(Transformation):
    is_global = True
    fields = {
        "fields": {"name": "Fields", "type": "list<string>", "required": False, "input": "column", "multiple": True,
                   "help": "The fields to use. Leave empty to use all.", "default": []},
        "axis": {"name": "Axis", "type": "string", "required": False, "input": "select", "multiple": False,
                 "default": "index", "help": "Over which axis should the values be calculated?",
                 "options": {"index": "Index", "columns": "Columns"}},
        "skipna": {"name": "Exclude NA/null values", "type": "string", "required": False, "input": "select",
                   "multiple": False, "help": "Should NA/null values be excluded?", "default": "1",
                   "options": {"1": "Yes", "0": "No"}},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.axis = arguments["axis"]
        self.skipna = arguments["skipna"] == "1"

    def __call__(self, rows: pd.DataFrame, index: int):
        raise NotImplemented


class Correlation(Transformation):
    is_global = True
    title = "Compute pairwise correlation of {fields}"
    key = "Correlation"
    fields = {
        "fields": StatsBase.fields["fields"],
        "method": {"name": "Method", "type": "string", "required": True, "input": "select",
                   "multiple": False, "help": "The method of correlation", "default": "pearson",
                   "options": {"pearson": "Pearson", "kendall": "Kendall", "spearman": "Spearman"}},
        "min_periods": {"name": "Minimum periods", "type": "number", "input": "number", "required": True,
                        "help": "The minimum number of observations for a valid result", "default": 1},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.method = arguments["method"]
        self.min_periods = int(arguments["min_periods"])

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]
        rows = rows.corr(method=self.method, min_periods=self.min_periods)
        return rows.reset_index().to_dict(orient="records"), index


class Covariance(Transformation):
    is_global = True
    title = "Compute pairwise covariance of {fields}"
    key = "Covariance"
    fields = {
        "fields": StatsBase.fields["fields"],
        "min_periods": Correlation.fields["min_periods"],
        "ddof": {"name": "Delta degrees of freedom", "type": "number", "input": "number", "required": True,
                 "help": "The divisor used in calculations is N - ddof, with N being the number of elements",
                 "default": 1},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.min_periods = int(arguments["min_periods"])
        self.ddof = int(arguments["ddof"])

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]
        rows = rows.cov(min_periods=self.min_periods, ddof=self.ddof)
        return rows.reset_index().to_dict(orient="records"), index


class CumSum(StatsBase):
    title = "Calculate the cumulative sum of {fields}"
    key = "Cumulative sum"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]
        return rows.cumsum(axis=self.axis, skipna=self.skipna).to_dict(orient="records"), index


class CumMax(StatsBase):
    title = "Calculate the cumulative maximum of {fields}"
    key = "Cumulative max"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]
        return rows.cummax(axis=self.axis, skipna=self.skipna).to_dict(orient="records"), index


class CumMin(StatsBase):
    title = "Calculate the cumulative minimum of {fields}"
    key = "Cumulative min"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]
        return rows.cummin(axis=self.axis, skipna=self.skipna).to_dict(orient="records"), index


class CumProd(StatsBase):
    title = "Calculate the cumulative product of {fields}"
    key = "Cumulative product"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]
        return rows.cumprod(axis=self.axis, skipna=self.skipna).to_dict(orient="records"), index


class Mad(StatsBase):
    title = "Calculate the mean absolute deviation of {fields}"
    key = "Mean absolute deviation (mad)"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]

        rows = rows.mad(axis=self.axis, skipna=self.skipna).rename("mad")
        rows = rows.reset_index() if self.axis == "index" else rows.to_frame()
        return rows.to_dict(orient="records"), index


class Skew(Transformation):
    is_global = True
    title = "Calculate the unbiased skew of {fields}"
    key = "Skew"
    fields = {
        "fields": StatsBase.fields["fields"],
        "axis": StatsBase.fields["axis"],
        "skipna": StatsBase.fields["skipna"],
        "numeric_only": {"name": "Numeric only", "type": "string", "required": False, "input": "select",
                         "multiple": False, "help": "Include only float, int, boolean columns?", "default": "0",
                         "options": {"1": "Yes", "0": "No"}},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.axis = arguments["axis"]
        self.skipna = arguments["skipna"] == "1"
        self.numeric_only = arguments["numeric_only"] == "1"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]

        rows = rows.skew(axis=self.axis, skipna=self.skipna, numeric_only=self.numeric_only).rename("skew")
        rows = rows.reset_index() if self.axis == "index" else rows.to_frame()
        return rows.to_dict(orient="records"), index


class Kurtosis(Skew):
    title = "Calculate the unbiased kurtosis of {fields}"
    key = "Kurtosis"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]

        rows = rows.kurtosis(axis=self.axis, skipna=self.skipna, numeric_only=self.numeric_only).rename("kurtosis")
        rows = rows.reset_index() if self.axis == "index" else rows.to_frame()
        return rows.to_dict(orient="records"), index


class Median(Skew):
    title = "Calculate the median of {fields}"
    key = "Median"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]

        rows = rows.median(axis=self.axis, dropna=self.skipna, numeric_only=self.numeric_only).rename("median")
        rows = rows.reset_index() if self.axis == "index" else rows.to_frame()
        return rows.to_dict(orient="records"), index


class Mode(Skew):
    title = "Calculate the mode of {fields}"
    key = "Mode"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]
        return rows.mode(axis=self.axis, dropna=self.skipna).to_dict(orient="records"), index


class Max(Skew):
    title = "Calculate the max of {fields}"
    key = "Max"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]

        rows = rows.max(axis=self.axis, skipna=self.skipna, numeric_only=self.numeric_only).rename("max")
        rows = rows.reset_index() if self.axis == "index" else rows.to_frame()
        return rows.to_dict(orient="records"), index


class Min(Skew):
    title = "Calculate the min of {fields}"
    key = "Min"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]

        rows = rows.min(axis=self.axis, skipna=self.skipna, numeric_only=self.numeric_only).rename("min")
        rows = rows.reset_index() if self.axis == "index" else rows.to_frame()
        return rows.to_dict(orient="records"), index


class Sum(Transformation):
    title = "Calculate the sum"
    key = "Sum"
    fields = {
        "fields": StatsBase.fields["fields"],
        "axis": StatsBase.fields["axis"],
        "skipna": StatsBase.fields["skipna"],
        "numeric_only": Skew.fields["numeric_only"],
        "min_count": {"name": "Minimum observations", "type": "number", "input": "number", "required": False,
                      "default": 0, "help": "The minimum number of non-missing observations."},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.axis = arguments["axis"]
        self.skipna = arguments["skipna"] == "1"
        self.numeric_only = arguments["numeric_only"] == "1"
        self.min_count = get_param_int(arguments["min_count"], 0)

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]

        rows = rows.sum(axis=self.axis, skipna=self.skipna, numeric_only=self.numeric_only, min_count=self.min_count)\
            .rename("sum")
        rows = rows.reset_index() if self.axis == "index" else rows.to_frame()
        return rows.to_dict(orient="records"), index


class Std(Transformation):
    title = "Calculate the standard deviation of {fields}"
    key = "Standard Deviation (std)"
    fields = {
        "fields": StatsBase.fields["fields"],
        "axis": StatsBase.fields["axis"],
        "skipna": StatsBase.fields["skipna"],
        "numeric_only": Skew.fields["numeric_only"],
        "ddof": Covariance.fields["ddof"],
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.axis = arguments["axis"]
        self.skipna = arguments["skipna"] == "1"
        self.numeric_only = arguments["numeric_only"] == "1"
        self.ddof = get_param_int(arguments["ddof"], 1)

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]

        rows = rows.std(axis=self.axis, skipna=self.skipna, numeric_only=self.numeric_only, ddof=self.ddof)\
            .rename("std")
        rows = rows.reset_index() if self.axis == "index" else rows.to_frame()
        return rows.to_dict(orient="records"), index


class Var(Std):
    title = "Calculate the variance of {fields}"
    key = "Variance (var)"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]

        rows = rows.var(axis=self.axis, skipna=self.skipna, numeric_only=self.numeric_only, ddof=self.ddof)\
            .rename("var")
        rows = rows.reset_index() if self.axis == "index" else rows.to_frame()
        return rows.to_dict(orient="records"), index


class Sem(Std):
    title = "Calculate the unbiased standard error of the mean in {fields}"
    key = "Standard error of mean (sem)"

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]

        rows = rows.sem(axis=self.axis, skipna=self.skipna, numeric_only=self.numeric_only, ddof=self.ddof)\
            .rename("var")
        rows = rows.reset_index() if self.axis == "index" else rows.to_frame()
        return rows.to_dict(orient="records"), index


class NUnique(StatsBase):
    title = "Get the number of unique values in {fields}"
    key = "Number of unique values (nunique)"
    fields = {
        "fields": StatsBase.fields["fields"],
        "axis": StatsBase.fields["axis"],
        "skipna": StatsBase.fields["skipna"],
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.output = arguments["output"]

    def __call__(self, rows: pd.DataFrame, index: int):
        if len(self.fields) > 0:
            rows = rows[self.fields]

        rows = rows.nunique(axis=self.axis, dropna=self.skipna).rename(self.output)
        rows = rows.reset_index() if self.axis == "index" else rows.to_frame()
        return rows.to_dict(orient="records"), index


class ValueCounts(Transformation):
    title = "Get the number of values in {fields}"
    key = "Value counts"
    fields = {
        "fields": StatsBase.fields["fields"],
        "normalize": {"name": "Normalize", "type": "string", "required": True, "input": "select", "default": "0",
                      "multiple": False, "help": "Return proportions rather than frequencies",
                      "options": {"1": "Yes", "0": "No"}},
        "sort": {"name": "Sort", "type": "string", "required": False, "input": "select", "default": "1",
                 "multiple": False, "help": "Should the values be sorted?", "options": {"1": "Yes", "0": "No"}},
        "order": {"name": "Order", "type": "string", "help": "",
                  "required": True, "input": "select", "multiple": False, "default": "asc",
                  "options": {"asc": "Ascending", "desc": "Descending"}, "optional": {"sort": ["1"]}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.normalize = arguments["normalize"] == "1"
        self.sort = arguments["sort"] == "1"
        self.ascending = arguments["order"] == "asc"
        self.output = arguments["output"]

    def __call__(self, rows: pd.DataFrame, index: int):
        subset = None
        if len(self.fields) > 0:
            subset = self.fields

        rows = rows\
            .value_counts(subset=subset, normalize=self.normalize, sort=self.sort, ascending=self.ascending)\
            .rename(self.output)\
            .reset_index()

        return rows.to_dict(orient="records"), index
