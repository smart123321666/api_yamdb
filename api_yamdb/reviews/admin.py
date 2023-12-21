from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment
from users.models import CustomUser

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('pk', 'name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('pk', 'name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score',
                    'pub_date')
    search_fields = ('pk', 'author', 'pub_date',)
    list_filter = ('author', 'pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author',
                    'review', 'pub_date')
    search_fields = ('pk', 'username',)
    list_filter = ('author', 'pub_date',)
    empty_value_display = '-пусто-'


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'confirmation_code',
                    'first_name', 'last_name', 'role', 'bio', 'password',)
    search_fields = ('username',)
    list_filter = ('username',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'
