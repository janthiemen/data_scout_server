from .connector import Connector
from .csv import CSV
from .excel import Excel
from .data_source_type import DataSourceType
from .big_query import BigQuery

DATA_SOURCE_MAP = {
    "CSV": CSV,
    "Excel": Excel,
    "BigQuery": BigQuery
}
