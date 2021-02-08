from django.core.exceptions import ValidationError
from django.db import models

"""
User profile
Billing accounts
Projects
User projects
"""


# Create your models here.
class DataSourceFolder(models.Model):
    name = models.CharField(max_length=512)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="child_folders")


class DataSource(models.Model):
    name = models.CharField(max_length=512)
    # We have the option to create a "tree" structure, where we can set the parent of a data source
    parent = models.ForeignKey(DataSourceFolder, on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    # The type of the data source (e.g. BigQuery, Csv, Excel, etc.)
    source = models.CharField(max_length=512)
    # The arguments to pass to the data source, defined as a JSON string
    kwargs = models.TextField()

    schema = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class RecipeFolder(models.Model):
    name = models.CharField(max_length=512)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="child_folders")


class Recipe(models.Model):
    SAMPLING_TECHNIQUE_CHOICES = (
        ('top', 'Top'),
        ('random', 'Random'),
        ('stratified', 'Stratified'),
    )

    name = models.CharField(max_length=512)
    parent = models.ForeignKey(RecipeFolder, on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    input = models.ForeignKey(DataSource, on_delete=models.CASCADE, null=True, blank=True, related_name="recipe_input")
    input_join = models.ForeignKey('Join', on_delete=models.CASCADE, null=True, blank=True, related_name="recipe_join")
    output = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="recipe_output", null=True)
    sampling_technique = models.CharField(
        max_length=64,
        choices=SAMPLING_TECHNIQUE_CHOICES,
        default="top",
    )
    schema = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Transformation(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="transformations")

    # We'll link the transformation steps together by defining a "previous", which links to another transformation
    previous = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="next")
    # The name of the transformation to apply
    transformation = models.CharField(max_length=512)
    # The arguments to pass to the transformation, defined as a JSON string
    kwargs = models.TextField()


class Join(models.Model):
    name = models.CharField(max_length=512)
    data_source_left = models.ForeignKey(DataSource, null=True, blank=True, on_delete=models.CASCADE,
                                         related_name="join_data_source_left")
    recipe_left = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.CASCADE,
                                    related_name="join_recipe_left")
    data_source_right = models.ForeignKey(DataSource, null=True, blank=True, on_delete=models.CASCADE,
                                          related_name="join_data_source_right")
    recipe_right = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.CASCADE,
                                     related_name="join_recipe_right")

    JOIN_METHOD_CHOICES = (
        ('inner', 'Inner'),
        ('outer', 'Outer'),
        ('left', 'Left'),
        ('right', 'Right'),
        ('cross', 'Cartesian product'),
    )

    method = models.CharField(max_length=512, choices=JOIN_METHOD_CHOICES, default="inner",)
    field_left = models.TextField()
    field_right = models.TextField()
    parent = models.ForeignKey(DataSourceFolder, on_delete=models.CASCADE, null=True, blank=True,
                               related_name="child_joins")

    def clean(self):
        super().clean()
        if (self.data_source_left is None and self.recipe_left is None) or \
                (self.data_source_left is not None and self.recipe_left is not None):
            raise ValidationError('You need a data source OR a pipeline on the left')
        if (self.data_source_right is None and self.recipe_right is None) or \
                (self.data_source_right is not None and self.recipe_right is not None):
            raise ValidationError('You need a data source OR a pipeline on the right')

        # TODO: Add a check for recursion!


class UserFile(models.Model):
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="files")
    field_name = models.CharField(max_length=1024)
    file_name = models.CharField(max_length=1024, null=True)
    original_file_name = models.CharField(max_length=1024, null=True)
    # TODO: Add some sort of on delete

