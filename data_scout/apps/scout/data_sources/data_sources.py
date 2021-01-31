from .csv import CSV
from .big_query import BigQuery


class DataSourceTypeSerializer:
    data_source_types = {"BigQuery": BigQuery, "CSV": CSV}

    def serialize(self):
        serialized = []
        for data_source_type in self.data_source_types.values():
            serialized.append({"name": data_source_type.__name__, "fields": data_source_type.fields})

        return serialized
