from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'email', 'bio', 'role',)


class CustomUserCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError(f'Логин {username} недоступен')
        return username


class CodeConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
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
        allow_null=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genre'] = [{'name': genre.name, 'slug': genre.slug}
                                   for genre in instance.genre.all()]
        representation['category'] = {'name': instance.category.name, 'slug':
                                      instance.category.slug}
        return representation


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
        if self.instance is None:
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
