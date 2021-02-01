from .transformation import Transformation


class Keys(Transformation):
    title = "Get the keys of the dictionary in {field}"
    key = "Dictionary get keys"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to format", "column_type": ["dict"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = list(row[self.field].keys())
        except:
            row[self.output] = 0
        return row, index


class Values(Transformation):
    title = "Get the values of the dictionary in {field}"
    key = "Dictionary get value"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to format", "column_type": ["dict"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = list(row[self.field].values())
        except:
            row[self.output] = 0
        return row, index


class Get(Transformation):
    title = "Get the value of the dictionary in {field} for key {key}"
    key = "Dictionary get"
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The column to format", "column_type": ["dict"],
                  "required": True, "input": "column", "multiple": False, "default": ""},
        "key": {"name": "Key", "type": "string", "help": "The key to get from the dictionary", "column_type": ["dict"],
                "required": True, "input": "text", "multiple": False, "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.field = arguments["field"]
        self.key = arguments["key"]
        self.output = arguments["output"]

    def __call__(self, row, index: int):
        try:
            row[self.output] = row[self.field].get(self.key)
        except:
            row[self.output] = None
        return row, index


class Create(Transformation):
    title = "Create a dictionary field"
    key = "Dictionary creat"
    fields = {
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
        "items": {"name": "Items", "type": "list<agg>", "help": "The items of the dictionary",
                  "required": True, "input": "multiple", "multiple": True, "default": [],
                  "sub_fields": {
                      "name": {"name": "Name", "type": "string", "help": "The key of this column in the dictionary",
                               "required": True, "input": "text", "multiple": False, "default": ""},
                      "field": {"name": "Input", "type": "string", "help": "The column to use as input",
                                "required": True, "input": "column", "multiple": False, "default": ""},
                  }}
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        super().__init__(arguments, sample_size, example)
        self.output = arguments["output"]
        self.items = arguments["items"]

    def __call__(self, row, index: int):
        row[self.output] = {item["name"]: row.get(item["field"]) for item in self.items}
        return row, index
