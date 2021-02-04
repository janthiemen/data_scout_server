import csv
import random
import sys
from typing import List

import pandas as pd

from .connector import Connector


class CSV(Connector):
    """
    Read data from a CSV file.
    """
    TMP_SINK = False
    MAX_SIZE = 2000000
    MAX_ROWS = 200
    fields = {
        "filename": {"name": "Filename", "type": "file", "input": "file", "help": "The filename of the CSV file.",
                     "required": True},
        "delimiter": {"name": "Delimiter", "type": "string", "input": "text", "help": "The delimiter in the CSV file.",
                      "required": True, "default": ","},
        "has_header": {"name": "Has header", "type": "boolean", "input": "switch", "required": True, "default": False,
                       "help": "Does the file have a header containing the column names?."},
        "encoding": {"name": "Encoding", "type": "string", "input": "select", "options": ["UTF-8", "latin-1"],
                     "default": "UTF-8", "help": "The encoding of the CSV file.", "required": True,
                     "is_advanced": True},
    }

    def __init__(self, arguments):
        """Initialize the data source with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        super().__init__(arguments)
        self.filename = arguments["filename"]
        self.delimiter = arguments["delimiter"]
        self.has_header = arguments["has_header"]
        self.encoding = arguments["encoding"]

    def __call__(self, sample: bool = False, sampling_technique: str = "top", column_types: bool = False) -> List[dict]:
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
            with open(self.filename, encoding=self.encoding) as f:
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
            return df.to_dict(orient="records")
        else:
            # TODO: To be implemented properly!
            # raise NotImplementedError()

            df = pd.read_csv(self.filename, sep=self.delimiter, encoding=self.encoding,
                             header='infer' if self.has_header else None)
            return df.to_dict(orient="records")
