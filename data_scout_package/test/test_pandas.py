import unittest


class TextExample(unittest.TestCase):
    """
    Example test case.
    """

    def setUp(self) -> None:
        """
        Set up required parts.
        :return:
        """
        self.one = 1

    def test_one(self) -> None:
        """
        Test whether one equals 1.
        :return:
        """
        self.assertEqual(self.one, 1, msg="1 should equal 1")


if __name__ == "__main__":
    test = TextExample()
    test.setUp()
    test.test_one()
