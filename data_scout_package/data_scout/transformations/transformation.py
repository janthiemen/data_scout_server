class Transformation:
    title = None
    # If "filter = True", the call method should return False in case a certain row should be deleted
    filter = False
    # If the transformation is global, it's called at the dataset as a whole, if it's not, it's called per-row
    is_global = False
    # If "is_flatten == True", the call method is expected to return lists of rows instead of just rows
    is_flatten = False
    fields = {}
    allowed_sampling_techniques = ['random', 'stratified', 'top']

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        pass

    def spark(self, row):
        # TODO: If a method needs to do something else in Spark, override this method
        # TODO: We're always setting index to -1, this will FAIL for index-based filtering
        return self.__call__(row, -1)[0]

    def __call__(self, row, index: int):
        raise NotImplementedError
