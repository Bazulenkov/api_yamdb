from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .models import Review, Comment, Title
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def set_title_rating(self, title_id):
        title = get_object_or_404(id=title_id)
        title.rating = self.queryset.aggregate(Avg("score"))
        title.save()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        # проверка, чтобы не вылетало исключения, если rewview на title уже существует
        if title.reviews.filter(author=self.request.user).exists():
            raise serializers.ValidationError(
                "Отзыв от Вас на это произведение уже существует. Пользователь может оставить только один отзыв на один объект.",
                code=400,
            )

        # проверка, чтобы score был 1..10 - надо дописывать или будет автоматом из-за ограничения в сериализаторе?
        serializer.save(title=title, author=self.request.user)
        self.set_title_rating(self.kwargs.get("title_id"))

    def perform_destroy(self, instance):
        instance.delete()
        self.set_title_rating(self.kwargs.get("title_id"))

    def perform_update(self, serializer):
        serializer.save()
        self.set_title_rating(self.kwargs.get("title_id"))


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        if not Title.objects.get(id=self.kwargs.get("title_id")).exists():
            raise NotFound(detail=_("Title not found"), code=404)

        # title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review = get_object_or_404(
            Review, id=self.kwargs.get("review_id"), title__id=self.kwargs.get("title_id")
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review = get_object_or_404(
            Review, id=self.kwargs.get("review_id"), title__id=self.kwargs.get("title_id")
        )
        serializer.save(title=title, review=review, author=self.request.user)
