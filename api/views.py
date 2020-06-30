from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        reviews = Review.objects.filter(title__id=title_id)
        return reviews


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
