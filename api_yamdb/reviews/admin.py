# ice_cream/admin.py
from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


admin.site.empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'genre',
        'category'
    )
    """ list_editable = (
        'category'
    ) """
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    """ list_editable = (
        'category'
    ) """
    search_fields = ('author',)
    list_filter = ('pub_date',)
    list_display_links = ('text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
    )


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)