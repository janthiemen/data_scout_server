import csv
import random
import sys
from typing import List

import openpyxl
import pandas as pd
from sqlalchemy import create_engine

from .connector import Connector


class SQL(Connector):
    """
    Read data from a SQL database.
    """
    TMP_SINK = False
    MAX_ROWS = 200
    fields = {
        "connection_string": {"name": "Connection string", "type": "string", "input": "text", "required": True,
                              "help": "The SQL Alchemy connection string "
                                      "(https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls)."},
        "sql": {"name": "SQL query", "type": "string", "input": "text-area", "required": True, "default": "",
                "help": "The SQL query to execute. Should NOT have a LIMIT query."},
    }

    def __init__(self, arguments):
        """Initialize the data source with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        super().__init__(arguments)
        self.connection_string = arguments["connection_string"]
        self.sql = arguments["sql"]

    def __call__(self, sample: bool = False, sampling_technique: str = "top", column_types: bool = False) -> List[dict]:
        """This class is called when the data needs to be loaded.

        Arguments:
            :type sample: boolean: Whether to take a sample or not
            :type sampling_technique: str: Which sampling technique to use (top)

        Returns:
            dict -- The row, including the extra output column
        """
        sql = self.sql
        if sample:
            sql = sql + f" LIMIT {self.MAX_ROWS}"
        # TODO: To be implemented properly!
        # raise NotImplementedError()
        sql_engine = create_engine(self.connection_string, echo=False)
        connection = sql_engine.raw_connection()
        data = pd.read_sql(sql, connection).to_dict(orient="records")
        connection.close()
        return data
