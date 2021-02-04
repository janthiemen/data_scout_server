from typing import List

import pandas as pd

from .connector import Connector


class Join(Connector):
    """
    Join two pipelines.
    """

    def __init__(self, arguments):
        """Initialize the data source with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        super().__init__(arguments)
        self.left = arguments["left"]
        self.right = arguments["right"]
        self.on_left = arguments["on_left"]
        self.on_right = arguments["on_right"]
        self.how = arguments["how"]

    def spark(self, sample: bool = False, sampling_technique: str = "top", column_types: bool = False):
        raise NotImplementedError()

    def __call__(self, sample: bool = False, sampling_technique: str = "top", column_types: bool = False) -> List[dict]:
        """This class is called when the data needs to be loaded.

        Arguments:
            :type sample: boolean: Whether to take a sample or not - IGNORED
            :type sampling_technique: str: Which sampling technique to use (top) - IGNORED

        Returns:
            dict -- The row, including the extra output column
        """
        # TODO: To be implemented properly!
        # raise NotImplementedError()
        df_left = pd.DataFrame(self.left(sample, sampling_technique, False)[0])
        df_right = pd.DataFrame(self.right(sample, sampling_technique, False)[0])
        data = df_left.merge(df_right, left_on=self.on_left, right_on=self.on_right, how=self.how)
        return data.to_dict(orient="records")
