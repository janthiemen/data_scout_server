class Add:
    fields = {
        "fields": {"name": "Fields", "type": "list<string>", "help": "The fields to add to each other",
                   "required": True, "input": "column", "multiple": True},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results"},
    }

    def __init__(self, arguments):
        """Initialize the transformation with the given parameters.
        
        Arguments:
            arguments {dict} -- The arguments
        """        
        self.fields = arguments["fields"]
        self.output = arguments["output"]

    def __call__(self, row):
        """This class is called on each row.
        
        Arguments:
            row {dict} -- The complete row
        
        Returns:
            dict -- The row, including the extra output column
        """
        total = 0
        for field in self.fields:
            total += row[field]

        row[self.output] = total
        return row


class Min:
    fields = {
        "field_a": {"name": "Field 1", "type": "string", "help": "The field that should be subtracted from",
                    "required": True, "input": "column", "multiple": False},
        "field_b": {"name": "Field 2", "type": "string", "help": "The field that should be subtracted",
                    "required": True, "input": "column", "multiple": False},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results"},
    }

    def __init__(self, arguments):
        """Initialize the transformation with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        self.field_a = arguments["field_a"]
        self.field_b = arguments["field_b"]
        self.output = arguments["output"]

    def __call__(self, row):
        """This class is called on each row.

        Arguments:
            row {dict} -- The complete row

        Returns:
            dict -- The row, including the extra output column
        """

        row[self.output] = row[self.field_a] - row[self.field_b]
        return row


class Divide:
    fields = {
        "field_a": {"name": "Numerator", "type": "string", "help": "The numerator",
                    "required": True, "input": "column", "multiple": False},
        "field_b": {"name": "Denominator", "type": "string", "help": "The denominator",
                    "required": True, "input": "column", "multiple": False},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results"},
    }

    def __init__(self, arguments):
        """Initialize the transformation with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        self.field_a = arguments["field_a"]
        self.field_b = arguments["field_b"]
        self.output = arguments["output"]

    def __call__(self, row):
        """This class is called on each row.

        Arguments:
            row {dict} -- The complete row

        Returns:
            dict -- The row, including the extra output column
        """

        # TODO: Add check on division by 0?
        row[self.output] = row[self.field_a] / row[self.field_b]
        return row


class Multiply:
    fields = {
        "fields": {"name": "Fields", "type": "list<string>", "help": "The fields to add to each other",
                   "required": True, "input": "column", "multiple": True},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results"},
    }

    def __init__(self, arguments):
        """Initialize the transformation with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        self.fields = arguments["fields"]
        self.output = arguments["output"]

    def __call__(self, row):
        """This class is called on each row.

        Arguments:
            row {dict} -- The complete row

        Returns:
            dict -- The row, including the extra output column
        """
        total = None
        for field in self.fields:
            if total is None:
                total = row[field]
            else:
                total *= row[field]

        row[self.output] = total
        return row


class Convert:
    fields = {
        "field": {"name": "Field", "type": "string", "help": "The field to convert", "required": True,
                  "input": "column", "multiple": False},
        "to": {"name": "To", "type": "string", "help": "To which data type to convert", "required": True,
               "input": "select", "multiple": False,
               "options": {"int": "Integer", "float": "Floating point number", "string": "Text"}}
    }

    def __init__(self, arguments):
        """Initialize the transformation with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        self.field = arguments["field"]
        self.to = arguments["to"]

    def __call__(self, row):
        """This class is called on each row.

        Arguments:
            row {dict} -- The complete row

        Returns:
            dict -- The row, including the extra output column
        """
        if self.to == "int":
            row[self.field] = int(row[self.field])
        elif self.to == "float" or self.to == 'Floating point number':
            row[self.field] = float(row[self.field])
        return row


TRANSFORMATION_MAP = {
    "add": Add,
    "min": Min,
    "convert": Convert,
    "multiply": Multiply,
    "divide": Divide,
}
