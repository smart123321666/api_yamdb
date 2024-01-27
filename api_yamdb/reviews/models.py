from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from api.validators import validate_year


User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=settings.MAX_TEXT_LENGTH,
        unique=True
    )
    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = [
            'slug',
        ]

    def __str__(self):
        return f'{self.name} {self.slug}'


class Genre(models.Model):
    name = models.CharField(
        'Наименование жанра',
        max_length=settings.MAX_TEXT_LENGTH,
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = [
            'slug',
        ]

    def __str__(self):
        return f'{self.name} {self.slug}'


class Title(models.Model):
    name = models.CharField(
        'Наименование произведения',
        max_length=settings.MAX_TEXT_LENGTH,
    )
    year = models.IntegerField(
        'Год',
        validators=[validate_year]
    )
    description = models.TextField(
        'Описание',
        blank=True

    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='title'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='title'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = [
            'name',
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        'Текст ревью',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    score = models.IntegerField(
        'Оценка',
        default=0,
        validators=[
            MaxValueValidator(settings.MAX_SCORE, ('''Оценка не может
                                   быть больше %(limit_value)s.''')),
            MinValueValidator(settings.MIN_SCORE, ('''Оценка не может
                                  быть ниже %(limit_value)s.''')),
        ]
    )
    pub_date = models.DateTimeField(
        'Время публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            UniqueConstraint(fields=['title', 'author'],
                             name='unique_title_author')
        ]
        ordering = [
            'pub_date',
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        'Текст коментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    pub_date = models.DateTimeField(
        'Время публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = [
            'pub_date',
        ]

    def __str__(self):
        return self.text
