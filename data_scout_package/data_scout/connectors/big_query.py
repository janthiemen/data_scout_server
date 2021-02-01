from data_scout.connectors.connector import Connector


class BigQuery(Connector):
    fields = {
        "project": {"name": "Project", "type": "string", "help": "The project from which to retrieve the data.",
                    "required": True},
        "test": {"name": "Test", "type": "number", "help": "The project from which to retrieve the data.",
                 "required": True, "min": 0, "max": 100},
        "dataset": {"name": "Data set", "type": "string",
                    "help": "The data set from which to retrieve the data. Either dataset and table or query should be filled out.",
                    "required": False},
        "table": {"name": "Table", "type": "string",
                  "help": "The table from which to retrieve the data. Either dataset and table or query should be filled out.",
                  "required": False},
        "query": {"name": "Query", "type": "string",
                  "help": "The query to use to retrieve the data. Either dataset and table or query should be filled out.",
                  "required": False},
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

    def __call__(self, sample: bool = False, sampling_technique: str = "top"):
        # TODO: Return the data (as a beam stream)
        pass
