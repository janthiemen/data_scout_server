import importlib
import subprocess
import sys
from typing import List

from .transformations import TRANSFORMATION_MAP


class Scout:
    """
    This is the main controller class. It manages all meta information, and installs/imports packages
    """

    def __init__(self, extensions: List[dict] = None):
        self.transformations = TRANSFORMATION_MAP
        self.extensions = extensions
        if self.extensions is not None:
            self.load_extensions()

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

