import itertools
from typing import List, Tuple, Type
import pandas as pd

from .connectors.data_source_type import DataSourceType
from .exceptions import TransformationUnavailableException
from .scout import Scout
from .transformations import _utils
from .transformations.data import MissingColumns, GetFields
from .transformations.transformation import Transformation


class Executor:

    def __init__(self, data_source: dict, pipeline: List[dict], scout: Scout):
        self.data_source = data_source
        self.pipeline = pipeline
        self.scout = scout

    def load_data(self, use_sample: bool = False, sampling_technique: str = "top") -> List[dict]:
        data_source = DataSourceType.get_by_string(self.data_source["source"])(self.data_source["kwargs"])
        data = data_source(use_sample, sampling_technique)
        return data

    def _make_dataframe(self, records: List[dict]):
        """
        Make a dataframe.
        :param records: The input records (list for Pandas, RDD for PySpark)
        :return:
        """
        raise NotImplementedError()

    def _get_columns(self, records: List[dict]) -> dict:
        """
        Get a list of column_name: column_type dicts.

        :param records: A list of all records
        :return: A list of column names and their types
        """
        raise NotImplementedError()

    def _apply(self, records, transformation: Transformation):
        raise NotImplementedError()

    def _apply_flatten(self, records, transformation: Transformation):
        """
        Apply a function that expands the records

        :param records:
        :return:
        """
        raise NotImplementedError()

    def _apply_global(self, records, transformation: Transformation):
        """
        Apply a function to all the records (group bys, etc.)

        :param records:
        :return:
        """
        raise NotImplementedError()

    def _filter(self, records):
        """
        Filter all elements that are False

        :param records:
        :return:
        """
        raise NotImplementedError()

    def _get_transformations(self) -> List[Tuple[int, dict, Type[Transformation]]]:
        t = 1
        transformation_list = []
        for step in self.pipeline:
            if step["transformation"] not in self.scout.transformations:
                raise TransformationUnavailableException(step["transformation"])
            else:
                transformation_list.append((t, step, self.scout.transformations[step["transformation"]]))
                t += 1
        return transformation_list

    def __call__(self, column_types: bool = False):
        columns = []
        transformation_list = self._get_transformations()

        # TODO:
        records = self.load_data(True, "top")
        for t, step, t_class in transformation_list:
            # Execute the transformation on the data set
            # TODO: only calculate length if the transformation requires it!
            sample_size = len(records)
            # Before each step we create a list of columns and column types that are available
            df_records = None
            if column_types:
                step_columns, df_records = _utils.get_columns(records)
                columns.append(step_columns)

            t_func = t_class(step["kwargs"], sample_size, records[0])
            # If it's a global transformation, we'll call it on all records, if it isn't, we call it one-at-a-time
            if t_func.is_global:
                if not column_types:
                    # If we're loading column types, this is already defined
                    df_records = self._make_dataframe(records)
                records = self._apply_global(df_records, t_func)
            elif t_func.is_flatten:
                records = self._apply_flatten(records, t_func)
            else:
                records = self._apply(records, t_func)
            if t_func.filter:
                records = self._filter(records)

            # TODO: Make sure we're still returning records, even if an error occurs
        return records


class PandasExecutor(Executor):

    def _apply(self, records, transformation: Transformation):
        for i, record in enumerate(records):
            records[i], _ = transformation(record, i)
        return records

    def _apply_global(self, df_records, transformation: Transformation):
        records, _ = transformation(df_records, -1)
        return records

    def _apply_flatten(self, records, transformation: Transformation):
        records = self._apply(records, transformation)
        return list(itertools.chain.from_iterable(records))

    def _get_columns(self, records: List[dict]) -> Tuple[dict, pd.DataFrame]:
        # TODO: Check if we can do this more efficient (without going back and forth between lists and dfs).
        df_records = self._make_dataframe(records)
        type_mappings = {
            "Timestamp": "datetime"
        }
        return {key: type_mappings.get(type(val).__name__, type(val).__name__) for key, val in
                df_records.to_dict(orient="records")[0].items()}, df_records

    def _make_dataframe(self, records: List[dict]):
        return pd.DataFrame(records)

    def _filter(self, records):
        def _is_false(value):
            return value != False

        return [record for record in filter(_is_false, records)]


class SparkExecutor(Executor):

    def _apply(self, records, transformation: Transformation):
        return records.map(transformation.spark)
        # return records.map(lambda x: {"a": x, "b": x})

    def _apply_global(self, df_records, transformation: Transformation):
        return transformation.spark(df_records)

    def _apply_flatten(self, rdd, transformation: Transformation):
        # TODO: Make sure that flatten transformations ALWAYS return a list
        return rdd.flatMap(transformation)

    def _get_columns(self, records: List[dict]) -> Tuple[dict, pd.DataFrame]:
        # TODO
        pass

    def _make_dataframe(self, records):
        get_fields = GetFields()
        columns = get_fields.spark(records)
        mc = MissingColumns({"columns": columns}, 0, None)
        records = self._apply(records, mc)
        return records.toDF()

    def _filter(self, records):
        return records.filter(lambda x: x != False)
