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
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        model = Title


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

    """ def validate(self, data):
        if len(data['name']) > 256:
            raise serializers.ValidationError(status=status.HTTP_400_BAD_REQUEST)
        return data """



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        fields = ['id', 'score', 'author', 'text', 'pub_date']
        model = Review
        read_only_fields = ('author', 'title', 'id', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        fields = ['id', 'author', 'text', 'pub_date']
        model = Comment
        read_only_fields = ('author', 'title', 'id', 'pub_date')
