from apps.scout.models import Recipe


class Transformation:
    title = None
    filter = False
    # If the transformation is global, it's called at the dataset as a whole, if it's not, it's called per-row
    is_global = False
    fields = {}
    allowed_sampling_techniques = [key for key, _ in Recipe.SAMPLING_TECHNIQUE_CHOICES]

    def __call__(self, row, index: int):
        raise NotImplementedError
