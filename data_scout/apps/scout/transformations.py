class Add:
    fields = {
        "fields": {"name": "Field 1", "type": "list<string>", "help": "The fields to add to each other",
                   "required": True, "input": "column", "multiple": False},
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
    "convert": Convert,
}
