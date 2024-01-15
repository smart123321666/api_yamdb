from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Comment, Category, Title, Review, Genre

from django.http import Http404
from django.db.models import Avg


User = get_user_model()


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.HyperlinkedModelSerializer):

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
        representation['genre'] = [{'name': genre.name, 'slug': genre.slug} for genre in instance.genre.all()]
        representation['category'] = {'name': instance.category.name, 'slug': instance.category.slug}
        return representation


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(default=None,)

    class Meta:
        model = Title
        fields = ['id', 'genre', 'category', 'name', 'year', 'description', 'rating']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ['id', 'score', 'author', 'text', 'pub_date']
        model = Review
        read_only_fields = ('id', 'pub_date', 'title')

    def create(self, validated_data):
        title_id = self.context['view'].kwargs['title_id']
        author = self.context.get('request').user
        try:
            title = Title.objects.get(id=title_id)
        except Title.DoesNotExist:
            raise Http404("Title matching query does not exist.")
        existing_rewiews = Review.objects.filter(title=title,
                                                 author=author).exists()
        if existing_rewiews:
            raise serializers.ValidationError('Вы уже оставили отзыв!')
        score = validated_data.pop('score')
        review = Review.objects.create(title=title,
                                       author=author,
                                       score=score,
                                       **validated_data)
        return review


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
