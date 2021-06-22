from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

########################################################################################################################
# IAM (users, projects, etc.)
########################################################################################################################


class Project(models.Model):
    """
    Every resource is part of a project.
    """
    name = models.CharField(max_length=512)


class UserProject(models.Model):
    """
    Users are added to projects using a user project object. This also defines the role of the user in the project.
    """
    ROLES = (
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    role = models.CharField(
        max_length=64,
        choices=ROLES,
        default="admin",
    )


class UserProfile(models.Model):
    """
    The user always has exactly 1 active project. This is defined in the user profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    project = models.ForeignKey(UserProject, null=True, blank=True, on_delete=models.SET_NULL)


########################################################################################################################
# Data scout
########################################################################################################################


class DataSourceFolder(models.Model):
    """
    Data sources are organized in data source folders. These form a tree based on the "parent" object. If no parent
    folder is set, it is a top level folder.
    """
    name = models.CharField(max_length=512)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="child_folders")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="data_source_folders")


class DataSource(models.Model):
    """
    A data source defines how data is loaded. This data source specific settings are stored as a JSON object in the
    kwargs field. The schema of the data set (column names and types) are stored in the schema field.
    """
    name = models.CharField(max_length=512)
    # We have the option to create a "tree" structure, where we can set the parent of a data source
    parent = models.ForeignKey(DataSourceFolder, on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    # The type of the data source (e.g. BigQuery, Csv, Excel, etc.)
    source = models.CharField(max_length=512)
    # The arguments to pass to the data source, defined as a JSON string
    kwargs = models.TextField()

    schema = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="data_sources")

    def __str__(self):
        return self.name


class RecipeFolder(models.Model):
    """
    Recipes are organized in recipe folders. These form a tree based on the "parent" object. If no parent folder is set,
    it is a top level folder.
    """
    name = models.CharField(max_length=512)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="child_folders")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="recipe_folders")


class Recipe(models.Model):
    """
    A recipe defines a flow. It has an input and an output data source. The latter is NOT used at the moment! The input
    can be either a data source, or join. A join has a data source or a recipe on one side on both sides. The schema of
    the flow's output (column names and types) are stored in the schema field.
    """
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="recipes")

    def __str__(self):
        return self.name


class Transformation(models.Model):
    """
    A transformation defines a step in the flow. This can be any of the transformations that are available in the Data
    Scout package. Its parameters are stored as JSON in the kwargs field.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="transformations")

    # We'll link the transformation steps together by defining a "previous", which links to another transformation
    previous = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="next")
    # The name of the transformation to apply
    transformation = models.CharField(max_length=512)
    # The arguments to pass to the transformation, defined as a JSON string
    kwargs = models.TextField()


class Join(models.Model):
    """
    A join combines two data sources/recipes. In the interface a join is treated as a data source. It can be used in the
    same way as an input to a recipe.
    """
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="joins")

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
    """
    Users are allowed to upload files. Those files are stored on disk, but a reference is store in a UserFile object.
    """
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="files")
    field_name = models.CharField(max_length=1024)
    file_name = models.CharField(max_length=1024, null=True)
    original_file_name = models.CharField(max_length=1024, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="user_files")
    # TODO: Add some sort of on delete

