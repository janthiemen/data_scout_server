from apps.scout.models import Recipe


class Transformation:
    title = None
    # If "filter = True", the call method should return False in case a certain row should be deleted
    filter = False
    # If the transformation is global, it's called at the dataset as a whole, if it's not, it's called per-row
    is_global = False
    # If "is_flatten == True", the call method is expected to return lists of rows instead of just rows
    is_flatten = False
    fields = {}
    allowed_sampling_techniques = [key for key, _ in Recipe.SAMPLING_TECHNIQUE_CHOICES]

    def __call__(self, row, index: int):
        raise NotImplementedError
