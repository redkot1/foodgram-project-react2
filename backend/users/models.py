from typing import Tuple

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(
        max_length=254, unique=True, verbose_name='Адрес электорной почты'
    )
    username = models.CharField(
        max_length=150, unique=True, verbose_name='Nickname'
    )
    first_name = models.CharField(
        max_length=150, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150, verbose_name='Фамилия')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower', verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following', verbose_name='Автор'
    )

    class Meta:
        ordering: Tuple[str] = ('user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return str(self.author)
