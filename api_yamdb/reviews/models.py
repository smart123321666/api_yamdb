from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


MAXIMUM_LENGHT_OF_HEDERS = 256


class Category(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=200,
        unique=True
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.slug}'


class Genre(models.Model):
    name = models.CharField(
        'Наименование жанра',
        max_length=50,
        unique=True
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.slug}'


class Title(models.Model):
    name = models.CharField(
        'Наименование произведения',
        max_length=200
    )
    year = models.IntegerField(
        'Год'
    ) # Возможно нужно поменять на DateField
    description = models.TextField(
        'Описание',
        max_length=MAXIMUM_LENGHT_OF_HEDERS,
        null=True,
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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        'Текст ревью',
        max_length=MAXIMUM_LENGHT_OF_HEDERS
    )
    author = models.IntegerField(
        'Автор'
    )
    score = models.IntegerField(
        'Оценка',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    pub_date = models.DateTimeField(
        'Время публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)

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
        max_length=MAXIMUM_LENGHT_OF_HEDERS
    )
    author = models.IntegerField(
        'Автор'
    )
    pub_date = models.DateTimeField(
        'Время публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ('pub_date',)
