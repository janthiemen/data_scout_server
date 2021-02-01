import itertools

from .groupby import GroupByBase
import pandas as pd


class Window(GroupByBase):
    is_global = True
    title = "Create a rolling window"
    key = "Rolling window"
    fields = {
        "index_type": {"name": "Index type", "type": "string", "required": True, "input": "select", "multiple": False,
                       "help": "What should the windowing be based on?", "default": "observations",
                       "options": {"observations": "# of observations", "datetime": "Date/time"}},
        "size": {"name": "Size", "type": "number", "help": "The size of the window", "required": True,
                 "input": "number", "multiple": False, "default": 2},
        "time": {"name": "Time", "type": "string", "required": True, "input": "select", "multiple": False,
                 "help": "The unit type of the size", "default": "T", "optional": {"index_type": ["datetime"]},
                 "options": {"D": "Days", "H": "Hours", "T": "Minutes", "S": "Seconds", "L": "Milliseconds",
                             "U": "Microseconds", "N": "Nanoseconds"}},
        "field_datetime": {"name": "Field", "type": "string", "help": "The field to use as input", "required": False,
                           "column_type": ["datetime"], "input": "column", "multiple": False, "default": "",
                           "optional": {"index_type": ["datetime"]}},
        "orientation": {"name": "Orientation", "type": "string", "required": False, "input": "select",
                        "multiple": False, "help": "Should the window be forward or backward looking?",
                        "default": "backward", "options": {"backward": "Backward", "forward": "Forward"},
                        "optional": {"index_type": ["observations"]}},
        "aggs": GroupByBase.fields["aggs"]
    }

    def _add_aggregation(self, name, field, function):
        if field not in self.aggregations:
            self.aggregations[field] = []
            self.column_names[field] = []
        self.aggregations[field].append(function)
        self.column_names[field].append(name)

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        self.column_names = {}
        super().__init__(arguments, sample_size, example)
        self.index_type = arguments["index_type"]
        self.size = int(arguments["size"])
        self.time = arguments["time"]
        self.field_datetime = arguments["field_datetime"]
        self.orientation = arguments["orientation"]

    def __call__(self, rows: pd.DataFrame, index: int):
        if self.index_type == "datetime":
            rows = rows.set_index(self.field_datetime).sort_index()
            window = f"{self.size}{self.time}"
        else:
            if self.orientation == "forward":
                window = pd.api.indexers.FixedForwardWindowIndexer(window_size=self.size)
            else:
                window = self.size

        rows = rows.rolling(window=window).agg(self.aggregations)
        rows.columns = list(itertools.chain.from_iterable(self.column_names.values()))
        return rows.reset_index().to_dict(orient="records"), index
