from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import (
    Buylist, Ingredient, Favorite, Product, Recipe, Tag
)
from users.serializers import ProfileSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ingredient


class IngredientRepresentationSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        fields = '__all__'
        model = Product


class ProductSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), validators=[
            UniqueValidator(queryset=Ingredient.objects.all())
        ]
    )
    amount = serializers.IntegerField(min_value=0)

    class Meta:
        model = Product
        fields = ('id', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):

    tags = TagSerializer(
        many=True, read_only=True
    )
    author = ProfileSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        queryset = Product.objects.filter(recipe=obj)
        return IngredientRepresentationSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Buylist.objects.filter(
            user=request.user, recipe=obj).exists()


class RecipeRepresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image',
                  'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):

    ingredients = ProductSerializer(many=True)
    author = ProfileSerializer(read_only=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(min_value=0)

    class Meta:
        fields = '__all__'
        read_only_fields = ('author',)
        model = Recipe

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'Такой ингредиент уже выбран'
                })
            ingredients_list.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError({
                    'amount': 'Количество не может быть отрицательным'
                })

        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Нужно выбрать тэг'
            })
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError({
                    'tags': 'Такой тэг уже есть'
                })
            tags_list.append(tag)

        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError({
                'cooking_time': 'Время не может быть отрицательным'
            })
        return data

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            Product.objects.create(
                recipe=recipe, ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    def create_tags(self, tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        author = validated_data.pop('author')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(
            instance, context=context).data

    def update(self, instance, validated_data):
        instance.tags.clear()
        Product.objects.filter(recipe=instance).all().delete()
        self.create_tags(validated_data.pop('tags'), instance)
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)


class BuylistSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Buylist

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeRepresentationSerializer(
            instance.recipe, context=context).data


class FavoritesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Favorite

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeRepresentationSerializer(
            instance.recipe, context=context).data
