from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

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
    #category = CategorySerializer(many=True)
    genre = GenreSerializer(many=True)
    """ genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        #read_only=True,
        slug_field='name',
        default=GenreSerializer(many=True),
    ) """
    category = serializers.SlugRelatedField(
        #many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Comment
