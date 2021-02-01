
class DataSourceConnectorUnavailableException(BaseException):
    def __init__(self, connector: str, message: str = "The requested data source connector is not available"):
        self.connector = connector
        super().__init__(message)


class TransformationUnavailableException(BaseException):
    def __init__(self, transformation: str, message: str = "The requested transformation is not available"):
        self.transformation = transformation
        super().__init__(message)


class IndexFilterException(Exception):
    message = "An error occurred while filtering"

