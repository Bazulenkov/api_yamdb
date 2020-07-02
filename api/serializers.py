from rest_framework import serializers

from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name", "slug"]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ["name", "slug"]


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ["id", "name", "year", "rating", "description", "genre", "category"]
