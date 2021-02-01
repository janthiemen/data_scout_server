from typing import List

import pandas as pd

from .transformation import Transformation
from .groupby import GroupByBase
from .window import Window


class Pivot(GroupByBase):
    is_global = True
    title = "Pivot the data"
    key = "Pivot"
    fields = {
        "columns": {"name": "Columns", "type": "list<string>", "required": True, "input": "column", "multiple": True,
                    "help": "The columns whose values are pivoted to columns", "default": []},
        "index": {"name": "Index", "type": "list<string>", "help": "The columns that are used as the index",
                  "required": False, "input": "column", "multiple": True, "default": []},
        "fill_value": {"name": "Fill value", "type": "number", "help": "The value to fill missing fields with",
                       "required": False, "input": "number", "multiple": False, "default": ""},
        "dropna": {"name": "Drop NA", "type": "string", "required": True, "input": "select", "multiple": False,
                   "help": "Should missing values be dropped?", "default": "yes",
                   "options": {"yes": "Yes", "no": "No"}},
        "aggs": Window.fields["aggs"]
    }
    # TODO: Check if we want all aggs/if they all should be available here

    def _add_aggregation(self, name, field, function):
        if field not in self.aggregations:
            self.aggregations[field] = []
            self.column_names[field] = []
        self.aggregations[field].append(function)
        self.column_names[field].append(name)

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        self.column_names = {}
        super().__init__(arguments, sample_size, example)
        self.columns = arguments["columns"]
        self.index = arguments["index"]
        try:
            self.fill_value = float(arguments["fill_value"])
        except ValueError:
            self.fill_value = None
        self.dropna = arguments["dropna"] == "yes"

    def _make_column_names(self, columns: pd.MultiIndex) -> List[str]:
        """
        Make column names based on the aggregations in the pivot table.

        :param columns: The Pandas multilevel columns
        :return: A list of flat column names
        """
        flat_columns = []
        for col in columns:
            if col[1] == "<lambda>":
                i = 0
            else:
                i = int(col[1].replace("<lambda_", "").replace(">", ""))

            if len(col) > 2:
                column_name = self.column_names[col[0]][i] + "_" + "_".join(col[2:])
            else:
                column_name = self.column_names[col[0]][i]
            flat_columns.append(column_name)
        return flat_columns

    def __call__(self, rows: pd.DataFrame, index: int):
        rows = rows.pivot_table(index=self.index, columns=self.columns, aggfunc=self.aggregations,
                                fill_value=self.fill_value, dropna=self.dropna)
        if len(self.index) == 0:
            # When there are no index columns, the aggregations are used as index
            rows = rows.set_index(pd.Index(self._make_column_names(rows.index), name="Aggregation"))
            rows = rows.rename(columns={cols: "_".join(cols) for cols in rows.columns})
        else:
            rows.columns = self._make_column_names(rows.columns)
        return rows.reset_index().to_dict(orient="records"), index


class Unpivot(Transformation):
    is_global = True
    title = "Unpivot the data"
    key = "Unpivot"
    fields = {
        "id_vars": {"name": "Index columns", "type": "list<string>", "required": True, "input": "column",
                    "multiple": True, "help": "The column(s) to use as identifier variables.", "default": []},
        "value_vars": {"name": "Value columns", "type": "list<string>", "required": False, "input": "column",
                       "help": "Column(s) to unpivot. If empty, uses all columns that are not set as index columns.",
                       "multiple": True, "default": []},
        "var_name": {"name": "Variable name", "type": "string", "help": "The name of the variable column",
                     "required": True, "input": "text", "multiple": False, "default": ""},
        "value_name": {"name": "Value name", "type": "string", "help": "The name of the value column",
                       "required": True, "input": "text", "multiple": False, "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.id_vars = arguments["id_vars"]
        self.value_vars = arguments["value_vars"] if len(arguments["value_vars"]) > 0 else None
        self.var_name = arguments["var_name"]
        self.value_name = arguments["value_name"]

    def __call__(self, rows: pd.DataFrame, index: int):
        rows = rows.melt(id_vars=self.id_vars, value_vars=self.value_vars, var_name=self.var_name,
                         value_name=self.value_name)
        return rows.to_dict(orient="records"), index
