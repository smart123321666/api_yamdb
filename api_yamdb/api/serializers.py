from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Category, Title, Review, Genre

from rest_framework import status


User = get_user_model()


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    def create(self, instance, validated_data):
        categoy_data = validated_data.pop('gategory')
        genre_data = validated_data.pop('genre')
        category = Category.objects.get(slug=categoy_data['slug'])
        genre = Genre.objects.get(slug=genre_data['slug'])
        title = Title.objects.create(category=category, genre=genre, **validated_data)
        return title
    
    """ genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        allow_null=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    ) """
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        model = Title
    
    """ def validate(self, data):
        if len(data['name']) > 256:
            raise serializers.ValidationError(status=status.HTTP_400_BAD_REQUEST)
        return data """



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username'
    )

    class Meta:
        fields = ['id', 'score', 'author', 'text', 'pub_date']
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username'
    )

    class Meta:
        fields = ['id', 'author', 'text', 'pub_date']
        model = Comment