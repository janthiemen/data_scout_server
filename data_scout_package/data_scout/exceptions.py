
class DataSourceConnectorUnavailableException(BaseException):
    def __init__(self, connector: str, message: str = "The requested data source connector is not available"):
        self.connector = connector
        super().__init__(message)


class TransformationUnavailableException(BaseException):
    def __init__(self, transformation: str, message: str = "The requested transformation is not available"):
        self.transformation = transformation
        super().__init__(message)


class PipelineException(BaseException):
    """
    This exception is used as a "catch all". It includes a message, the original exception type and the transformation.
    """
    def __init__(self, transformation: int, original_exception: Exception,
                 message: str = "An error occurred while running the pipeline"):
        self.transformation = transformation
        self.original_exception = original_exception
        super().__init__(message)


class IndexFilterException(Exception):
    message = "An error occurred while filtering"

