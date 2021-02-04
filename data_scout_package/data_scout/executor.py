import itertools
from typing import List, Tuple, Type, Any, Optional
import pandas as pd

from .connectors.data_source_type import DataSourceType
from .connectors.join import Join
from .exceptions import TransformationUnavailableException, IndexFilterException, PipelineException
from .scout import Scout
from .transformations.data import MissingColumns, GetFields
from .transformations.transformation import Transformation


class Executor:
    """
    This is the abstract executor. It contains the base method every executor should implement.
    """

    def __init__(self, data_source: dict, pipeline: List[dict], scout: Scout):
        self.scout = scout
        self.pipeline = pipeline
        if data_source["source"] == "join":
            # If the data source is a join, the kwargs should hold a JSON definition
            # We only allow complete pipeline definitions as join tables. If you want to use just a raw data source,
            # enter an empty list as transformations.
            self.data_source = Join({
                "left": self.__class__(data_source=data_source["kwargs"]["left"]["data_source"],
                                       pipeline=data_source["kwargs"]["left"]["pipeline"], scout=self.scout),
                "right": self.__class__(data_source=data_source["kwargs"]["right"]["data_source"],
                                        pipeline=data_source["kwargs"]["right"]["pipeline"], scout=self.scout),
                "on_left": data_source["kwargs"]["on_left"],
                "on_right": data_source["kwargs"]["on_right"],
                "how": data_source["kwargs"]["how"],
            })
        else:
            self.data_source = self.scout.get_data_source(data_source["source"])(data_source["kwargs"])

    def join(self, left, right, on_left: List[str], on_right: List[str], how: str):
        raise NotImplementedError()

    def load_data(self, use_sample: bool = False, sampling_technique: str = "top") -> List[dict]:
        data = self.data_source(use_sample, sampling_technique, False)
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
        if use_sample:
            sampling_technique = self._get_sampling_technique(sampling_technique, transformation_list)
        records = self.load_data(use_sample, sampling_technique)
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
    """
    Execute a pipeline in Pandas.
    """

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


class CodeExecutor(Executor):

    def _get_columns(self, records: List[dict]) -> Tuple[dict, Any]:
        return {}, None

    def __init__(self, data_source: dict, pipeline: List[dict], scout: Scout):
        super().__init__(data_source, pipeline, scout)
        self.data_source = data_source
        self.pipeline = pipeline
        self.scout = scout

    def load_data(self, use_sample: bool = False, sampling_technique: str = "top") -> str:
        data_source_name = self._class_name(self.scout.get_data_source(self.data_source["source"]))
        data_source_params = str(self.data_source["kwargs"])

        code = f"data_source = {data_source_name}({data_source_params})\n"
        code += f"records = data_source(False, '{sampling_technique}')\n"
        return code

    def _apply(self, records, transformation: Optional[Transformation]) -> str:
        code = "for i, record in enumerate(records):\n"
        code += "    records[i], _ = transformation(record, i)\n"
        return code

    def _apply_global(self, df_records, transformation: Optional[Transformation]):
        code = "records, _ = transformation(df_records, -1)\n"
        return code

    def _apply_flatten(self, records, transformation: Optional[Transformation]):
        code = self._apply(records, transformation)
        code += "list(itertools.chain.from_iterable(records))\n"
        return code

    def _fix_missing_columns(self, records):
        code = self._make_dataframe(records)
        code += f"records = df_records.to_dict(orient='records')\n"
        return code

    def _make_dataframe(self, records: List[dict]):
        return "df_records = pd.DataFrame(records)\n"

    def _filter(self, records):
        code = "records = [record for record in filter(_is_false, records)]\n"
        return code

    def _make_data_source(self):
        # TODO
        pass

    def _class_name(self, o):
        """
        Get the fully classified class name of a certain type.

        :param o: The class
        :return:
        """
        module = o.__module__
        if module is None or module == str.__module__:
            return o.__name__  # Avoid reporting __builtin__
        else:
            return module + '.' + o.__name__

    def __call__(self, use_sample: bool = True, sampling_technique: str = 'top', column_types: bool = False):
        """
        Create a piece of code that will execute all of the steps in Pandas.

        :param use_sample: Not used
        :param sampling_technique: Not used
        :param column_types: Not used
        :return: A string containing the code and an empty list.
        """
        transformation_list = self._get_transformations()
        code = "import data_scout\n\n"
        code += "def _is_false(value):\n"
        code += "    return value != False\n\n"
        code += self.load_data(use_sample, sampling_technique)
        for t, step, t_class in transformation_list:
            # Execute the transformation on the data set
            code += f"sample_size = len(records)\n"
            code += f"transformation = {self._class_name(t_class)}({str(step['kwargs'])}, sample_size, records[0])\n"
            if t_class.is_global:
                code += self._make_dataframe([])
                code += self._apply_global(None, None)
            elif t_class.is_flatten:
                code += self._apply_flatten(None, None)
            else:
                code += self._apply(None, None)

            if t_class.filter:
                code += self._filter(None)

            code += "\n"
        return code, []


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
