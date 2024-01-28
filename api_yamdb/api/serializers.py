from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from api.validators import validate_username
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'email', 'bio', 'role',)


class CustomUserCreationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=settings.MAX_USERNAME_LENGTH,
                                     validators=[UnicodeUsernameValidator(),
                                                 validate_username])
    email = serializers.EmailField(required=True,
                                   max_length=settings.MAX_EMAIL_LENGTH)

    class Meta:
        model = User
        fields = ('email', 'username')


class CodeConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=settings.MAX_USERNAME_LENGTH,
                                     validators=[UnicodeUsernameValidator(),
                                                 validate_username])
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleSerializerCreateUpdate(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ['id', 'genre', 'category',
                  'name', 'year', 'description']

    def to_representation(self, value):
        return TitleSerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(default=None,)

    class Meta:
        model = Title
        fields = ['id', 'genre', 'category',
                  'name', 'year', 'description', 'rating']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ['id', 'score', 'author', 'text', 'pub_date']
        model = Review

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        author = self.context.get('request').user
        if self.context['request'].method == 'POST':
            existing_reviews = Review.objects.filter(title_id=title_id,
                                                     author=author).exists()
            if existing_reviews:
                raise serializers.ValidationError('Вы уже оставили отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        fields = ['id', 'author', 'text', 'pub_date']
        model = Comment
