class Transformation:
    title = None
    filter = False
    fields = {}

    def __call__(self, row):
        raise NotImplementedError
