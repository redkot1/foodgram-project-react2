from typing import Tuple

from django.db import models

from users.models import User


class Tag(models.Model):

    name = models.CharField(
        max_length=64, unique=True, verbose_name='Название'
    )
    color = models.CharField(
        max_length=24, unique=True, verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=30, unique=True, verbose_name='Слаг'
    )

    class Meta:
        ordering: Tuple[str] = ('-id',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):

    name = models.CharField(
        max_length=254, verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=64, verbose_name='Единицы измерения'
    )

    class Meta:
        ordering: Tuple[str] = ('-id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name[:15]


class Recipe(models.Model):

    name = models.CharField(max_length=64, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='Автор'
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Тэги'
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='Product', verbose_name='Ингредиенты'
    )
    image = models.ImageField(
        upload_to='recipes/', null=True, verbose_name='Изображение'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления'
    )

    class Meta:
        ordering: Tuple[str] = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name[:28]


class Product(models.Model):

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='product', verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT,
        related_name='product', verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        ordering: Tuple[str] = ('-recipe',)
        verbose_name = 'Количество ингредиента рецепта'
        verbose_name_plural = 'Состав и количество ингредиентов рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_list_ingredient_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredient} {self.amount}'


class Favorite(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Рецепт'
    )

    class Meta:
        ordering: Tuple[str] = ('-id',)
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_favorite'
            )
        ]

    def __str__(self) -> str:
        return str(self.recipe)


class Buylist(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='buy_list', verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='buy_list', verbose_name='Рецепт')

    class Meta:
        ordering: Tuple[str] = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_buylist'
            )
        ]

    def __str__(self) -> str:
        return str(self.recipe)
