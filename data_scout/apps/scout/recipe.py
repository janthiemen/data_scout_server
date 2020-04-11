from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Recipe


def get_recipe(recipe: int):
    return get_object_or_404(Recipe, pk=recipe)


def get_data(recipe: int):
    pass
