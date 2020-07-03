from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as VE
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db.models import Avg
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.models import Category, Genre, Title, Review, Comment
from api.permissions import IsAdmin
from api.serializers import (
    UserForAdminSerializer,
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
)

User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def generate_confirmation_code(request):
    email = request.data.get("email")
    if email is None:
        raise ValidationError({"email": "This field is required"})
    try:
        validate_email(email)
    except VE:
        raise ValidationError({"email": "Enter a valid email address."})
    username = email.split("@")[0]
    user = User.objects.filter(username=username).first()
    if not user:
        user = User.objects.create_user(username=username, email=email,)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        "Письмо с кодом подтверждения для доступа на YamDB",
        confirmation_code,
        "admin@yamdb.fake",
        [email],
    )
    return Response({"email": email})


@api_view(["POST"])
@permission_classes([AllowAny])
def get_tokens_for_user(request):
    email = request.data.get("email")
    confirmation_code = request.data.get("confirmation_code")
    if not confirmation_code:
        raise ValidationError({"confirmation_code": "This field is required"})
    user = generics.get_object_or_404(User, email=email)
    context = {"confirmation_code": "Enter a valid confirmation code"}
    if default_token_generator.check_token(user=user, token=confirmation_code):
        refresh = RefreshToken.for_user(user)
        context = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    return Response(context)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserForAdminSerializer
    permission_classes = [IsAuthenticated]  # , IsAdmin]
    lookup_field = "username"
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "=username",
    ]


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class CategoriesList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = [
        "=name",
    ]


class CategoryDestroy(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class GenresList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = [
        "=name",
    ]


class GenreDestroy(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    # filter_backends = [DjangoFilterBackend, ]
    ordering_fields = ["name"]

    def perform_create(self, serializer):
        category = generics.get_object_or_404(
            Category, slug=self.request.data.get("category")
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist("genre")
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        title = self.get_object()
        category = generics.get_object_or_404(
            Category, slug=self.request.data.get("category")
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist("genre")
        )
        title.genre.set(genre)
        serializer.save()
        title.category = category
        # title.save()
        # serializer.save()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = generics.get_object_or_404(
            Title, id=self.kwargs.get("title_id")
        )
        return title.reviews.all()

    def set_title_rating(self, title_id):
        title = generics.get_object_or_404(Title, id=title_id)
        title.rating = (
            self.get_queryset().aggregate(Avg("score")).get("score__avg")
        )
        title.save()

    def perform_create(self, serializer):
        title = generics.get_object_or_404(
            Title, id=self.kwargs.get("title_id")
        )
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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = generics.get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id"),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = generics.get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id"),
        )
        serializer.save(review=review, author=self.request.user)
