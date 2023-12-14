from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField() # Возможно нужно поменять на DateField
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category_titles'
    )
    genre = models.ManyToManyField(Genre)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title',
    )
    text = models.TextField()
    author = models.IntegerField()
    score = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.IntegerField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
