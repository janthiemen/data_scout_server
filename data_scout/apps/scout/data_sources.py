import csv
import os
import random
import sys

import pandas as pd
from django.conf import settings


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
    MAX_SIZE = 2000000
    MAX_ROWS = 200
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

    def __call__(self, sample: bool = False, sampling_technique: str = "top"):
        """This class is called when the data needs to be loaded.
        
        Arguments:
            :type sample: boolean: Whether to take a sample or not
            :type sampling_technique: str: Which sampling technique to use (top, stratisfied, random)

        Returns:
            dict -- The row, including the extra output column
        """
        # TODO: Return the data (as a beam stream or a pandas data frame (in case it's a sample))
        if sample:
            # TODO: Make this big data proof (chucking, sampling before loading, etc.)
            with open(os.path.join(settings.MEDIA_ROOT, self.filename), encoding=self.encoding) as f:
                number_of_rows = sum(1 for line in f)

                # We'll return to the start
                f.seek(0)
                row_sizes = []
                for line in f:
                    # We'll test the first 25 rows to determine average row size
                    row_sizes.append(sys.getsizeof(line))

                    # We want to check at least 25 rows, at most 250 and ideally 1%
                    if len(row_sizes) > max(min(number_of_rows * 0.01, 250), 25):
                        break

                sample_size = min(self.MAX_ROWS, round(self.MAX_SIZE / (sum(row_sizes) / len(row_sizes))))
                column_names, data = [], []

                f.seek(0)
                reader = csv.reader(f, delimiter=self.delimiter)
                i = 0

                if sampling_technique == "top":
                    # We'll just take the top rows
                    for row in reader:
                        if i == 0 and self.has_header:
                            column_names = row
                        elif i <= sample_size:
                            data.append(row)
                        else:
                            break
                        i += 1
                elif sampling_technique == "stratified":
                    # We'll take every xth row
                    stratified = round(number_of_rows / sample_size)
                    for row in reader:
                        if i == 0 and self.has_header:
                            column_names = row
                        elif i % stratified == 0:
                            data.append(row)
                        i += 1
                else:
                    # We're doing random sampling ...
                    rows_to_take = random.sample(range(1 if self.has_header else 0, number_of_rows), sample_size)
                    rows_to_take = sorted(rows_to_take)
                    for row in reader:
                        if i == 0 and self.has_header:
                            column_names = row
                        elif i == rows_to_take[0]:
                            data.append(row)
                            rows_to_take.pop(0)
                        if len(rows_to_take) == 0:
                            break
                        i += 1

            df = pd.DataFrame(data, columns=column_names)
            return df
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
