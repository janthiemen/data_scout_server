from django.db import models

"""
User profile
Billing accounts
Projects
User projects
"""


# Create your models here.
class DataSource(models.Model):
    name = models.CharField(max_length=512)
    # The type of the data source (e.g. BigQuery, Csv, Excel, etc.)
    source = models.CharField(max_length=512)
    # The arguments to pass to the data source, defined as a JSON string
    kwargs = models.TextField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=512)
    input = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="recipe_input")
    output = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="recipe_output")

    def __str__(self):
        return self.name


class Transformation(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
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
