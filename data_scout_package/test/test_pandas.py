import unittest

from data_scout.executor import PandasExecutor, CodeExecutor
from data_scout.scout import Scout


class TestPandas(unittest.TestCase):
    """
    Test the Pandas transformations.
    """

    def setUp(self) -> None:
        """
        Set up required parts.
        :return:
        """
        self.scout = Scout()
        self.executor = CodeExecutor({"source": "CSV", "kwargs": {
            "filename": "C:\\Users\\janthiemen.postema\\development\\data_scout\\data_scout\\uploads\\test.csv",
            "delimiter": ",",
            "encoding": "utf-8",
            "has_header": True
        }}, [{"transformation": "data-convert", "kwargs": {"field": "column1", "to": "int"}}], self.scout)

    def test_one(self) -> None:
        """
        Test whether one equals 1.
        :return:
        """
        print(self.executor())


if __name__ == "__main__":
    test = TestPandas()
    test.setUp()
    test.test_one()
