from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Comment, Category, Title, Review, Genre

from django.http import Http404
from django.db.models import Avg


User = get_user_model()


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



class TitleSerializerCreateUpdate(serializers.ModelSerializer):    # Переделать
    """ genre = serializers.SlugRelatedField(
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
        model = Title """
    
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ['id', 'genre', 'category', 'name', 'year', 'description', 'rating']
    
    def create(self, validated_data):
        print(self.context, '!!!!!!!!!!!!!!!!!!!!')
        genre = validated_data.pop('genre')
        category = validated_data.pop('category')
        title = Title.objects.create(**validated_data)

        return super().create(validated_data)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(default=None)

    class Meta:
        model = Title
        fields = ['id', 'genre', 'category', 'name', 'year', 'description', 'rating']
    
    def create(self, validated_data):
        print(self.context, '!!!!!!!!!!!!!!!!!!!!')
        genre = validated_data.pop('genre')
        category = validated_data.pop('category')
        title = Title.objects.create(**validated_data)

        return super().create(validated_data)
    
    """ def get_rating(self, obj):
        return int(obj.rating) """



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
            existing_reviews = Review.objects.filter(title_id=title_id, author=author).exists()
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