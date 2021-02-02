from data_scout.executor import PandasExecutor, CodeExecutor
from data_scout.scout import Scout

scout = Scout()
executor = CodeExecutor({"source": "CSV", "kwargs": {
    "filename": "C:\\Users\\janthiemen.postema\\development\\data_scout\\data_scout\\uploads\\test.csv",
    "delimiter": ",",
    "encoding": "utf-8",
    "has_header": True
    }}, [{"transformation": "data-convert", "kwargs": {"field": "column1", "to": "int"}}], scout)
print(executor()[0])
