from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.http import Http404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title

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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        fields = ['id', 'author', 'text', 'pub_date']
        model = Comment
        read_only_fields = ('id', 'pub_date')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ['id', 'genre', 'category',
                  'name', 'year', 'description', 'rating']

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(Avg('score'))['score__avg'], 2)
        return None
