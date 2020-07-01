from rest_framework import serializers

from .models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Review
        fields = ["id", "text", "author", "score", "pub_date"]
        read_only_fields = ["title"]


class Comment(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "pub_date"]
        read_only_fields = ["title", "review"]

