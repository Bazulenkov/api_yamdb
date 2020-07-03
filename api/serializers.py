from rest_framework import serializers
<<<<<<< HEAD
from django.contrib.auth import get_user_model


User = get_user_model()


class UserForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "first_name",
            "last_name",
            "username",
            "bio",
            "email",
            "role",
        )
        model = User


class UserSerializer(UserForAdminSerializer):
    role = serializers.CharField(read_only=True)
=======

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
>>>>>>> develop/titles-categories-genres/konstantin
