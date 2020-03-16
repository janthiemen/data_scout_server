from django.db import models

# Create your models here.
class DataSource(models.Model):
    # The type of the data source (e.g. BigQuery, Csv, Excel, etc.)
    source = None
    # The arguments to pass to the data source, defined as a JSON string
    kwargs = None

class Recipe(models.Model):
    name = models.CharField()

class Transformation(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    # The name of the transformation to apply
    transformation = None
    # The arguments to pass to the transformation, defined as a JSON string
    kwargs = None

class Flow(models.Model):
    name = models.CharField()

class FlowStep(models.Model):
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name="steps")

class Sink(models.Model):
    # The type of the data source. For intermittent sinking and joining, this data source must support SQL.
    source = None
    # The arguments to pass to the data source, defined as a JSON string
    kwargs = None

class Join(models.Model):
    data_source_left = None
    data_source_right = None
    # It's possible to create a join by selecting the fields to join on or by manually entering a join query
    method = None
    field_left = None
    field_right = None
    join_query = None

class Pipeline(models.Model):
    sink = models.ForeignKey(Sink, on_delete=models.CASCADE)
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE)
