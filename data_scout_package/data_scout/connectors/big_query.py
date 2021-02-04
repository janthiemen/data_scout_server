from data_scout.connectors.connector import Connector


class BigQuery(Connector):
    fields = {
        "project": {"name": "Project", "type": "string", "input": "text", "required": True,
                    "help": "The project from which to retrieve the data."},
        "test": {"name": "Test", "type": "number", "input": "number", "required": True, "min": 0, "max": 100,
                 "help": "The project from which to retrieve the data."},
        "dataset": {"name": "Data set", "type": "string", "input": "text", "required": False,
                    "help": "The data set from which to retrieve the data. Either dataset and table or query should be "
                            "filled out."},
        "table": {"name": "Table", "type": "string", "input": "text", "required": False,
                  "help": "The table from which to retrieve the data. Either dataset and table or query should be "
                          "filled out."},
        "query": {"name": "Query", "type": "string", "input": "text", "required": False,
                  "help": "The query to use to retrieve the data. Either dataset and table or query should be filled "
                          "out."},
    }

    def __init__(self, arguments: dict):
        """Initialize the data source with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        super().__init__(arguments)
        self.project = arguments["project"]
        self.dataset = arguments["dataset"]
        self.table = arguments["table"]
        self.query = arguments["query"]
        self.output = arguments["output"]

    def __call__(self, sample: bool = False, sampling_technique: str = "top", column_types: bool = False):
        # TODO: Return the data (as a beam stream)
        pass
