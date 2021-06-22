from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Recipe)
admin.site.register(models.RecipeFolder)
admin.site.register(models.Transformation)
admin.site.register(models.DataSource)
admin.site.register(models.UserFile)
admin.site.register(models.UserProfile)
admin.site.register(models.UserProject)
