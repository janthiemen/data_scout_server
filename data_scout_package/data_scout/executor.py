import itertools
from typing import List, Tuple, Type, Any
import pandas as pd

from .connectors.connector import Connector
from .connectors.data_source_type import DataSourceType
from .exceptions import TransformationUnavailableException, IndexFilterException, PipelineException
from .scout import Scout
from .transformations import _utils
from .transformations.data import MissingColumns, GetFields
from .transformations.transformation import Transformation


class Executor:

    def __init__(self, data_source: dict, pipeline: List[dict], scout: Scout):
        self.data_source = DataSourceType.get_by_string(data_source["source"])(data_source["kwargs"])
        self.pipeline = pipeline
        self.scout = scout

    def load_data(self, use_sample: bool = False, sampling_technique: str = "top") -> List[dict]:
        data = self.data_source(use_sample, sampling_technique)
        return data

    def _make_dataframe(self, records: List[dict]):
        """
        Make a dataframe.
        :param records: The input records (list for Pandas, RDD for PySpark)
        :return:
        """
        raise NotImplementedError()

    def _fix_missing_columns(self, records: List[dict]):
        """
        Make sure that each row in the dataset has the same keys.
        :param records: The input records (list for Pandas, RDD for PySpark)
        :return:
        """
        raise NotImplementedError()

    def _get_columns(self, records: List[dict]) -> Tuple[dict, Any]:
        """
        Get a list of column_name: column_type dicts.

        :param records: A list of all records
        :return: A list of column names and their types and a complete dataframe
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

    def _get_sampling_technique(self,
                                requested_technique: str,
                                transformation_list: List[Tuple[int, dict, Type[Transformation]]]):

        if len(transformation_list) == 0:
            # If there are no transformations, we can use all sampling techniques
            return requested_technique

        # Not every transformation can be used with all sampling techniques. We'll determine which is allowed.
        allowed_sampling_techniques = [transformation.allowed_sampling_techniques
                                       for _, _, transformation in transformation_list]

        result = set(self.data_source.SAMPLING_TECHNIQUES).intersection(*allowed_sampling_techniques)
        if requested_technique in result:
            return requested_technique
        elif len(result) == 0:
            self.scout.log.info(f"Couldn't find a sampling technique that satisfies all requirements. Using "
                                f"{requested_technique}, expect unexpected behaviour.")
            return requested_technique
        else:
            for key, _ in self.data_source.SAMPLING_TECHNIQUES:
                if key in result:
                    self.scout.log.info(f"Switched from sampling technique {requested_technique} to {key} because "
                                        f"of requirements by the transformations.")
                    return key

    def __call__(self, use_sample: bool = True, sampling_technique: str = 'top', column_types: bool = False):
        """
        Execute the pipeline that this executor was initialized with.

        :param use_sample: Should the data be sampled?
        :param sampling_technique: What sampling technique to use (only if use_sample is true)?
        :param column_types: Should the column types of all steps be returned? If not, an empty list is returned
        :return: A list of dictionary objects representing the data and a list of dicts representing the columns and
        column types.
        """
        columns = []
        transformation_list = self._get_transformations()
        # TODO:
        if use_sample:
            sampling_technique = self._get_sampling_technique(sampling_technique, transformation_list)
        records = self.load_data(use_sample, )
        for t, step, t_class in transformation_list:
            try:
                # Execute the transformation on the data set
                # TODO: only calculate length if the transformation requires it!
                sample_size = len(records)
                # Before each step we create a list of columns and column types that are available
                df_records = None
                if column_types:
                    step_columns, df_records = self._get_columns(records)
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
            except IndexFilterException as e:
                self.scout.log.warning(f"Transformation {t}: {e}")
            except TransformationUnavailableException as e:
                self.scout.log.warning(f"Transformation {t}: {e}")
            except Exception as e:
                raise PipelineException(transformation=t, original_exception=e)

        if column_types:
            step_columns, df_records = self._get_columns(records)
            columns.append(step_columns)

        records = self._fix_missing_columns(records)
        # TODO: Make sure we're still returning records, even if an error occurs
        return records, columns


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

    def _fix_missing_columns(self, records):
        return self._make_dataframe(records).to_dict(orient="records")

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

    def _fix_missing_columns(self, records):
        get_fields = GetFields()
        columns = get_fields.spark(records)
        mc = MissingColumns({"columns": columns}, 0, None)
        return self._apply(records, mc)

    def _make_dataframe(self, records):
        return self._fix_missing_columns(records).toDF()

    def _filter(self, records):
        return records.filter(lambda x: x != False)
