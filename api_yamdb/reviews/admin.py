from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

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
        'category',
    )
    filter_horizontal = (
        'genre',
    )
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
