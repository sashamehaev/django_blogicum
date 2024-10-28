from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel
from .constants import (
    POST_TITLE_MAX_LENGTH,
    LOCATION_NAME_MAX_LENGTH,
    CATEGORY_TITLE_MAX_LENGTH,
    ADMIN_POST_TITLE_MAX_LENGTH
)

User = get_user_model()


class Category(BaseModel):
    title = models.CharField('Заголовок', max_length=CATEGORY_TITLE_MAX_LENGTH)
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL;'
        + ' разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(
        'Название места',
        max_length=LOCATION_NAME_MAX_LENGTH
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(BaseModel):
    title = models.CharField('Заголовок', max_length=POST_TITLE_MAX_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        auto_now_add=False,
        help_text='Если установить дату и время '
        + 'в будущем — можно делать отложенные публикации.'
    )
    comment_count = models.IntegerField('Количество комментариев', default=0)
    image = models.ImageField('Фото', upload_to='post_images', blank=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Публикация'
        default_related_name = 'post'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:ADMIN_POST_TITLE_MAX_LENGTH]


class Comment(models.Model):
    text = models.TextField('Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.text
