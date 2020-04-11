import pandas as pd


class BigQuery:
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

    def __init__(self, arguments):
        """Initialize the data source with the given parameters.
        
        Arguments:
            arguments {dict} -- The arguments
        """
        self.project = arguments["project"]
        self.dataset = arguments["dataset"]
        self.table = arguments["table"]
        self.query = arguments["query"]
        self.output = arguments["output"]

    def __call__(self):
        """This class is called when the data needs to be loaded.
        
        Arguments:
        
        Returns:
            dict -- The row, including the extra output column
        """
        # TODO: Return the data (as a beam stream)
        pass


class CSV:
    """
    Read data from a CSV file.
    """
    TMP_SINK = False
    fields = {
        "filename": {"name": "Filename", "type": "string", "help": "The filename of the CSV file.", "required": True},
        "delimiter": {"name": "Delimiter", "type": "string", "help": "The delimiter in the CSV file.", "required": True,
                      "default": ","},
        "has_header": {"name": "Has header",
                       "type": "boolean",
                       "help": "Does the file have a header containing the column names?.",
                       "required": True,
                       "default": False},
        "encoding": {"name": "Encoding", "type": "select", "options": ["UTF-8", "latin-1"], "default": "UTF-8",
                     "help": "The encoding of the CSB file.", "required": True, "is_advanced": True},
    }

    def __init__(self, arguments):
        """Initialize the data source with the given parameters.
        
        Arguments:
            arguments {dict} -- The arguments
        """
        self.filename = arguments["filename"]
        self.delimiter = arguments["delimiter"]
        self.has_header = arguments["has_header"]
        self.encoding = arguments["encoding"]

    def __call__(self, sample=False):
        """This class is called when the data needs to be loaded.
        
        Arguments:
        
        Returns:
            dict -- The row, including the extra output column
        """
        # TODO: Return the data (as a beam stream or a pandas data frame (in case it's a sample))
        if sample:
            # TODO: Make this big data proof (chucking, sampling before loading, etc.)
            df = pd.read_csv(self.filename,
                             sep=self.delimiter,
                             header=0 if self.has_header else None,
                             encoding=self.encoding)
            return df.sample(n=250)
        else:
            # TODO: To be implemented
            raise NotImplementedError()


class DataSourceTypeSerializer:
    data_source_types = [BigQuery, CSV]

    def serialize(self):
        serialized = []
        for data_source_type in self.data_source_types:
            serialized.append({"name": data_source_type.__name__, "fields": data_source_type.fields})

        return serialized
