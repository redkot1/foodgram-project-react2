from django.contrib import admin

from .models import Ingredient, Tag, Product, Recipe

admin.site.register(Ingredient)

admin.site.register(Tag)

admin.site.register(Product)

admin.site.register(Recipe)
