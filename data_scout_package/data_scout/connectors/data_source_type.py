from typing import Type

from .sql import SQL
from .excel import Excel
from .connector import Connector
from .csv import CSV
from .big_query import BigQuery
from ..exceptions import DataSourceConnectorUnavailableException


class DataSourceType:
    data_source_types = {"BigQuery": BigQuery, "CSV": CSV, "Excel": Excel, "SQL": SQL}

    def serialize(self):
        serialized = []
        for data_source_type in self.data_source_types.values():
            serialized.append({"name": data_source_type.__name__, "fields": data_source_type.fields})

        return serialized

    @staticmethod
    def get_by_string(name: str) -> Type[Connector]:
        data_source = DataSourceType.data_source_types.get(name)
        if data_source is None:
            raise DataSourceConnectorUnavailableException(name)
        return data_source

