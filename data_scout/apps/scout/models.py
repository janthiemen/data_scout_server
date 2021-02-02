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
    input = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="recipe_input")
    output = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="recipe_output", null=True)
    sampling_technique = models.CharField(
        max_length=64,
        choices=SAMPLING_TECHNIQUE_CHOICES,
        default="top",
    )

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


class Flow(models.Model):
    name = models.CharField(max_length=512)
    sink = models.ForeignKey(DataSource, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Join(models.Model):
    data_source_left = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="join_data_source_left")
    data_source_right = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="join_data_source_right")
    # It's possible to create a join by selecting the fields to join on or by manually entering a join query
    method = models.CharField(max_length=512)
    field_left = models.CharField(max_length=1024)
    field_right = models.CharField(max_length=1024)
    join_query = models.TextField()


class FlowStep(models.Model):
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name="steps")
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, null=True)
    join = models.OneToOneField(Join, on_delete=models.CASCADE, null=True)


class UserFile(models.Model):
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="files")
    field_name = models.CharField(max_length=1024)
    file_name = models.CharField(max_length=1024, null=True)
    original_file_name = models.CharField(max_length=1024, null=True)
    # TODO: Add some sort of on delete


class TempDataSample(models.Model):
    """
    This table contains samples of the data sources. The actual samples are stored as CSV files on disk.
    """
    SAMPLING_TECHNIQUE_CHOICES = (
        ('random', 'Random'),
        ('stratified', 'Stratified'),
        ('top', 'Top'),
    )
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="samples")
    last_used = models.DateTimeField(auto_now=True)
    file_name = models.CharField(max_length=2048)
    sampling_technique = models.CharField(
        max_length=64,
        choices=SAMPLING_TECHNIQUE_CHOICES,
        default="top",
    )

    def __str__(self):
        return self.file_name
