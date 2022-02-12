from pathlib import Path

from django.db.models import Sum
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.filters import RecipeFilter, IngredientSearchFilter
from recipes.pagination import CustomPageNumberPagination
from recipes.serializers import (
    BuylistSerializer,
    TagSerializer,
    FavoritesSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeListSerializer,
)
from .models import (
    Buylist, Ingredient, Favorite, Product, Recipe, Tag
)


class TagViewSet(ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def add(self, request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def cancel(self, request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        obj_cart = get_object_or_404(
            model, user=user, recipe=recipe
        )
        obj_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['post'], permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        return self.add(request, pk, BuylistSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.cancel(request, pk, Buylist)

    @action(
        detail=True, methods=['post'], permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        return self.add(request, pk, FavoritesSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return self.cancel(request, pk, Favorite)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        objs = Product.objects.filter(
            recipe__buy_list__user=request.user).order_by('ingredient__name')
        ingredients = objs.values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_total=Sum('amount'))
        f_string = 'Список покупок:\n'
        for ingredient in ingredients:
            f_string += (
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["ingredient_total"]}'
                f'{ingredient["ingredient__measurement_unit"]}\n'
            )
        response = HttpResponse(f_string, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="output.txt"'
        return response
