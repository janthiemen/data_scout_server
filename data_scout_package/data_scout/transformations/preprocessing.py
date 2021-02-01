import pandas as pd
from sklearn import preprocessing
from .transformation import Transformation


class Scale(Transformation):
    title = "Scale {field} using a {method} scaler"
    key = "Scale"
    is_global = True
    fields = {
        "field": {"name": "Fields", "type": "string", "help": "The fields to scale","required": True, "input": "column",
                  "multiple": False, "default": "", "column_type": ["int", "float"]},
        "method": {"name": "Comparison", "type": "string", "help": "How should the values be compared?",
                   "required": True, "input": "select", "multiple": False, "default": "and",
                   "options": {"standard": "Standard", "minmax": "MinMax", "maxabs": "MaxAbs"}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.method = arguments["method"]
        self.output = arguments["output"]

    def __call__(self, rows: pd.DataFrame, index: int):
        if self.method == "standard":
            scaler = preprocessing.StandardScaler()
        elif self.method == "minmax":
            scaler = preprocessing.MinMaxScaler()
        elif self.method == "maxabs":
            scaler = preprocessing.MaxAbsScaler()
        else:
            raise ValueError(f"The selected scaling method ({self.method} is not available")

        rows[self.output] = scaler.fit_transform(rows[self.field].values.reshape(-1, 1))

        return rows.to_dict(orient="records"), index


class CategoricalEncoding(Transformation):
    title = "Encoding {field} using a {method} encoder"
    key = "Encode categorical features"
    is_global = True
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "method": {"name": "Comparison", "type": "string", "help": "How should the values be encoded?",
                   "required": True, "input": "select", "multiple": False, "default": "onehot",
                   "options": {"ordinal": "Ordinal", "onehot": "One-hot"}},
        "categories": {"name": "Categories", "type": "string", "required": False, "input": "text-area", "default": "",
                       "help": "An ordered list of all possible categories (one per line), optional",
                       "optional": {"method": ["ordinal"]}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.method = arguments["method"]
        self.categories = arguments["categories"].splitlines()
        if len(self.categories) == 0:
            self.categories = "auto"
        self.output = arguments["output"]

    def __call__(self, rows: pd.DataFrame, index: int):
        if self.method == "ordinal":
            encoder = preprocessing.OrdinalEncoder(categories=[self.categories])
            rows[self.output] = encoder.fit_transform(rows[self.field].values.reshape(-1, 1))
        elif self.method == "onehot":
            rows = pd.concat([rows, pd.get_dummies(rows[self.field], prefix=self.output)], axis=1)
        else:
            raise ValueError(f"The selected encoder ({self.method} is not available")

        return rows.to_dict(orient="records"), index


class DiscretizeBin(Transformation):
    title = "Discretize {field} into {k} bins"
    key = "Discretize"
    is_global = True
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "k": {"name": "Bins", "type": "number", "help": "The number of bins to divide the feature into",
              "required": True, "input": "number", "multiple": False, "default": 2},
        "encode": {"name": "Encoding", "type": "string", "help": "How should the bins be encoded?",
                   "required": True, "input": "select", "multiple": False, "default": "ordinal",
                   "options": {"ordinal": "Ordinal", "onehot-dense": "One-hot"}},
        "strategy": {"name": "Strategy", "type": "string", "help": "How should the bins be generated?",
                     "required": True, "input": "select", "multiple": False, "default": "quantile",
                     "options": {"uniform": "Uniform", "quantile": "Quantile", "kmeans": "K-Means"}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.k = int(arguments["k"])
        self.encode = arguments["encode"]
        self.strategy = arguments["strategy"]
        self.output = arguments["output"]

    def __call__(self, rows: pd.DataFrame, index: int):
        est = preprocessing.KBinsDiscretizer(n_bins=self.k, encode='ordinal', strategy=self.strategy)
        rows[self.output] = est.fit_transform(rows[self.field].values.reshape(-1, 1))
        if self.encode == "onehot":
            rows = pd.concat([rows, pd.get_dummies(rows[self.output], prefix=self.output)], axis=1)\
                .drop(self.output, axis=1)

        return rows.to_dict(orient="records"), index


class Binarize(Transformation):
    title = "Binarize {field} using {threshold} as threshold"
    key = "Binarize"
    is_global = True
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "threshold": {"name": "Threshold", "type": "number", "help": "The value to split the feature on",
                      "required": True, "input": "number", "multiple": False, "default": 0.0},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.threshold = float(arguments["threshold"])
        self.output = arguments["output"]

    def __call__(self, rows: pd.DataFrame, index: int):
        est = preprocessing.Binarizer(threshold=self.threshold)
        rows[self.output] = est.fit_transform(rows[self.field].values.reshape(-1, 1))
        return rows.to_dict(orient="records"), index


class Normalize(Transformation):
    title = "Normalize {field} using the {norm} norm"
    key = "Normalize"
    is_global = True
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "norm": {"name": "Norm", "type": "string", "help": "The norm to use",
                 "required": True, "input": "select", "multiple": False, "default": "l2",
                 "options": {"l1": "l1", "l2": "l2", "max": "max"}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.norm = arguments["norm"]
        self.output = arguments["output"]

    def __call__(self, rows: pd.DataFrame, index: int):
        est = preprocessing.Normalizer(norm=self.norm)
        rows[self.output] = est.fit_transform(rows[self.field].values.reshape(-1, 1))
        return rows.to_dict(orient="records"), index


class Polynomial(Transformation):
    is_global = True
    key = "Polynomial features"
    title = "Generate a polynomial feature based on {fields}"
    fields = {
        "fields": {"name": "Fields", "type": "list<string>", "help": "The fields to add to each other",
                   "required": True, "input": "column", "multiple": True, "default": "",
                   "column_type": ["int", "float"]},
        "degree": {"name": "Degree", "type": "number", "input": "number", "required": False, "default": 2,
                   "help": "The degree of the polynomial features"},
        "interaction_only": {"name": "Interaction only", "type": "string", "input": "select", "multiple": False,
                             "help": "Only include interaction features", "required": False, "default": "0",
                             "options": {"1": "Yes", "0": "No"}},
        "include_bias": {"name": "Include bias", "type": "string", "input": "select", "multiple": False,
                         "help": "Include a bias column (a column of ones)", "required": False, "default": "1",
                         "options": {"1": "Yes", "0": "No"}},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.fields = arguments["fields"]
        self.degree = int(arguments["degree"])
        self.interaction_only = arguments["interaction_only"] == "1"
        self.include_bias = arguments["include_bias"] == "1"
        self.output = arguments["output"]

    def __call__(self, rows: pd.DataFrame, index: int):
        trans = preprocessing.PolynomialFeatures(degree=self.degree, interaction_only=self.interaction_only,
                                                 include_bias=self.include_bias)
        rows_trans = pd.DataFrame(trans.fit_transform(rows[self.fields].values[:, :-1]))
        rows = pd.concat([rows, rows_trans.rename({col: f"{self.output}_{col}" for col in rows_trans.columns}, axis=1)],
                         axis=1)
        return rows.to_dict(orient="records"), index


class Impute(Transformation):
    title = "Impute {field} through {strategy}"
    key = "Impute missing values"
    is_global = True
    fields = {
        "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "strategy": {"name": "Strategy", "type": "string", "help": "The strategy to use",
                     "required": True, "input": "select", "multiple": False, "default": "mean",
                     "options": {"mean": "mean", "median": "median", "mode": "most frequent", "max": "max",
                                 "min": "min", "constant": "constant", "ffill": "Forward fill",
                                 "bfill": "Backward fill", "interpolate": "Interpolate"}},
        "type": {"name": "Constant type", "type": "string", "help": "The data type of the constant",
                 "required": False, "input": "select", "multiple": False, "default": "string",
                 "options": {"string": "String", "float": "Float", "int": "Integer"},
                 "optional": {"strategy": ["constant"]}},
        "constant_string": {"name": "Value", "type": "string", "input": "text", "required": False, "default": "",
                            "optional": {"strategy": ["constant"], "type": ["string"]},
                            "help": "The value to fill the column with"},
        "constant_number": {"name": "Value", "type": "number", "input": "number", "required": False, "default": "",
                            "optional": {"strategy": ["constant"], "type": ["int", "float"]},
                            "help": "The value to fill the column with"},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.strategy = arguments["strategy"]
        self.constant = ""
        if arguments["type"] == "string":
            self.constant = str(arguments["constant_string"])
        elif arguments["type"] == "int":
            self.constant = int(arguments["constant_number"])
        elif arguments["type"] == "float":
            self.constant = float(arguments["constant_number"])
        self.output = arguments["output"]

    def __call__(self, rows: pd.DataFrame, index: int):
        if self.strategy == "mean":
            rows[self.output] = rows[self.field].fillna(rows[self.field].mean())
        elif self.strategy == "mode":
            rows[self.output] = rows[self.field].fillna(rows[self.field].mode()[0])
        elif self.strategy == "median":
            rows[self.output] = rows[self.field].fillna(rows[self.field].median())
        elif self.strategy == "max":
            rows[self.output] = rows[self.field].fillna(rows[self.field].max())
        elif self.strategy == "min":
            rows[self.output] = rows[self.field].fillna(rows[self.field].min())
        elif self.strategy == "constant":
            rows[self.output] = rows[self.field].fillna(self.constant)
        elif self.strategy == "ffill":
            rows[self.output] = rows[self.field].ffill()
        elif self.strategy == "bfill":
            rows[self.output] = rows[self.field].bfill()
        elif self.strategy == "interpolate":
            rows[self.output] = rows[self.field].interpolate()
        else:
            raise ValueError(f"The selected strategy ({self.strategy} is not available")

        return rows.to_dict(orient="records"), index
