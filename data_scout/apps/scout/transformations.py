class Add:
    fields = {
        "fields": {"name": "Field 1", "type": "list<string>", "help": "The fields to add to each other", "required": True},
        "output": {"name": "Output column", "type": "string", "help": "The name of the (newly created) column that contains the results", "required": True},
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
            total += field

        row[self.output] = total
        return row

