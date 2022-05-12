from rest_framework import serializers
from reviews.models import Category, Genre, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    "Сериалайзер для Users."

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "bio",
        )
        lookup_field = "username"


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Category."""
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Genre."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Title."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Title при действии 'retrieve', 'list.'"""
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
