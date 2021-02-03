import logging
import subprocess
import sys
from typing import List, Type

from .connectors import DATA_SOURCE_MAP, Connector
from .transformations import TRANSFORMATION_MAP


class Scout:
    """
    This is the main controller class. It manages all meta information, and installs/imports packages
    """

    def __init__(self, logger: logging.Logger = None, extensions: List[dict] = None):
        self.transformations = TRANSFORMATION_MAP
        # TODO: Add option to install data sources
        self.data_sources = DATA_SOURCE_MAP
        self.log = logger
        if self.log is None:
            self.log = logging.getLogger(__name__)

        self.extensions = extensions
        if self.extensions is not None:
            self.load_extensions()

    def execute_json(self, definition: dict, executor_class):
        """
        Execute a JSON pipeline definition.

        :param definition: Dict containing: use_sample, sampling_technique, column_types, data_source, pipeline
        :param executor_class: A class that shall be initialized and called
        :return: The results of the executor
        """
        executor = executor_class(data_source=definition["data_source"], pipeline=definition["pipeline"], scout=self)
        return executor(use_sample=definition["use_sample"], sampling_technique=definition["sampling_technique"],
                        column_types=definition["column_types"])

    def load_extensions(self):
        """
        Load/install all extensions.

        :return:
        """
        for extension in self.extensions:
            self.load_extension(extension)

    def _import_module(self, module):
        globals()[module] = __import__(module)

    def load_extension(self, extension: dict):
        """
        Load/install an extensions and add its transformations to the transformation map.

        :param extension: A dict containing the package name, install path and a list of transformations
        :return:
        """
        try:
            self._import_module(extension['package'])
        except ModuleNotFoundError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", extension['install']])
            self._import_module(extension['package'])

        for transformation in extension["transformations"]:
            self.transformations[transformation["name"]] = eval(transformation["class"])

    def get_data_source(self, data_source: str) -> Type[Connector]:
        return self.data_sources.get(data_source)
