
from django.utils import timezone
from django.forms import ValidationError
from rest_framework import serializers

from reviews.models import Comment, Category, Title, Review, Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        allow_null=True,
        slug_field='name'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )

    class Meta:
        fields = '__all__'
        model = Title
def validate_year(value):
    current_year = timezone.now().year
    if value < 1900 or value > current_year:
        raise ValidationError(
            'Неверно указан год, не может быть меньше 1900 и больше текущего.'
        )
class TitleCreateAndUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор создания или редактирования произведения."""

    genre = serializers.SlugRelatedField(
        slug_field='name', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all()
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Comment
