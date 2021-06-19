Getting Started
======================================

There are two ways to use this tool. Either as a standalone package that runs hand-made or previously exported pipelines, or in combination with the Data Scout Server, which provides a WYSIWYG tool for creating data preparation pipelines that can be executed by this package, in one of the available runner environments. Currently only vanilla Python is available, but PySpark should be available soon.

This section focuses on the standalone package. If you'd like to learn more about installing the server, go to `this page <server.html>`__. For more information on how to use the data wrangler tool, go to the `usage page <usage.html>`__.

Installation
------------
The easiest and quickest way to install Data Scout is through PyPi, just execute the following command::

    pip install data-scout


Executing a JSON pipeline
+++++++++++++++++++++++++

Pipeline definitions can be given as JSON files or directly as Python commands. To execute a JSON definition, your code would look somewhat as follows::

    scout = Scout()
    executor = PandasExecutor({"source": "CSV", "kwargs": {
        "filename": "test.csv",
        "delimiter": ",",
        "encoding": "utf-8",
        "has_header": True
    }}, [{"transformation": "data-convert", "kwargs": {"field": "column1", "to": "int"}}], scout)
    executor()

This will load a CSV file and convert the column named "column1" to an integer using Pandas as a backend.

Executing Python code
+++++++++++++++++++++
If you'd like to execute the Python code directly, the sample above would look somewhat as follows::

    import data_scout

    def _is_false(value):
        return value != False

    data_source = data_scout.connectors.csv.CSV({'filename': 'test.csv', 'delimiter': ',', 'encoding': 'utf-8', 'has_header': True})
    records = data_source(False, 'top')
    sample_size = len(records)
    transformation = data_scout.transformations.data.Convert({'field': 'column1', 'to': 'int'}, sample_size, records[0])
    for i, record in enumerate(records):
        records[i], _ = transformation(record, i)


Running the server
------------------

There are two ways to run the data scout server. The easiest option is through Docker. This will automatically spin up the server, create a database and setup the frontend. The other option is to run the server manually with your own database. Here we'll only discuss the former. If you'd like to go the manual root, have a look at the server documentation here.

TODO: Docker explanation


