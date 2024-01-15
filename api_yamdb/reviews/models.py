import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator



MAXIMUM_LENGHT_OF_HEDERS = 256


User = get_user_model()


def validate_year(value):
    current_year = datetime.datetime.now().year
    if value > current_year:
        raise ValidationError("Год не может быть больше текущего года.")


class Category(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
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
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
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
        max_length=256,
    )
    year = models.IntegerField(
        'Год',
        validators=[validate_year]
    )
    description = models.TextField(
        'Описание'
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
            MaxValueValidator(10, ('Оценка не может быть больше %(limit_value)s.')),
            MinValueValidator(0, ('Оценка не может быть ниже %(limit_value)s.')),
        ]
    )
    pub_date = models.DateTimeField(
        'Время публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('title', 'author')
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
