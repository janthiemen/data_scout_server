from typing import List


class Connector:
    SAMPLING_TECHNIQUES = ['random', 'stratified', 'top']
    fields = {}

    def __init__(self, arguments: dict):
        """Initialize the data source with the given parameters.

        Arguments:
            arguments {dict} -- The arguments
        """
        pass

    def __call__(self, sample: bool = False, sampling_technique: str = "top", column_types: bool = False) -> List[dict]:
        """This class is called when the data needs to be loaded.

        Arguments:
            :type sample: boolean: Whether to take a sample or not
            :type sampling_technique: str: Which sampling technique to use (top, stratisfied, random)

        Returns:
            dict -- The row, including the extra output column
        """
        raise NotImplementedError()
