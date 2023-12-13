from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class UserApi(AbstractUser):
    bio = models.TextField('Биография', blank=True) 



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
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.IntegerField()
    title = models.OneToOneField(
        Title,
        on_delete=models.CASCADE,
        related_name='title',
        blank=True,
        null=True
    )
    score = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.IntegerField()
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('created',)