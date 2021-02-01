from .transformation import Transformation
import pandas as pd


class SortBy(Transformation):
    is_global = True
    title = "Sort the data"
    key = "Sort"
    fields = {
        "sorting": {"name": "Sort by:", "type": "list<agg>", "help": "The columns to sort by",
                    "required": True, "input": "multiple", "multiple": True, "default": [],
                    "sub_fields": {
                        "field": {"name": "Column", "type": "string", "help": "The column to sort by",
                                  "required": True, "input": "column", "multiple": False, "default": ""},
                        "order": {"name": "Order", "type": "string", "help": "The order to sort in",
                                  "required": True, "input": "select", "multiple": False, "default": "asc",
                                  "options": {"asc": "Ascending", "desc": "Descending"}},
                    }},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.by = [sort["field"] for sort in arguments["sorting"]]
        self.asc = [sort["order"] == "asc" for sort in arguments["sorting"]]

    def __call__(self, rows: pd.DataFrame, index: int):
        return rows.sort_values(by=self.by, ascending=self.asc).to_dict(orient="records"), index
