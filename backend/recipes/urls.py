from django.urls import include, path
from rest_framework import routers

from recipes.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet
)

router = routers.DefaultRouter()
router.register(
    'tags', TagViewSet, basename='tags'
)
router.register(
    'recipes', RecipeViewSet, basename='recipes'
)
router.register(
    'ingredients', IngredientViewSet, basename='ingredients'
)

urlpatterns = [
    path('', include(router.urls)),
]
