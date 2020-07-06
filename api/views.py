from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as VE
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import IntegrityError
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.models import Category, Genre, Title, Review
from api.permissions import (
    IsAdminOrReadOnly,
    IsAdminRole,
    IsStaffOrOwnerOrReadOnly,
)
from api.viewsets import ListCreateDestroyViewSet
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
    user = User.objects.get_or_create(username=username, email=email)
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
    permission_classes = [IsAdminRole]
    lookup_field = "username"
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "=username",
    ]

    @action(methods=["get", "patch"], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, pk=None):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesViewset(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewset(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]
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
        self.perform_create(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsStaffOrOwnerOrReadOnly]

    def get_queryset(self):
        title = generics.get_object_or_404(
            Title, id=self.kwargs.get("title_id")
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        try:
            title = generics.get_object_or_404(
                Title, id=self.kwargs.get("title_id")
            )
            serializer.save(title=title, author=self.request.user)
        except IntegrityError:
            raise ValidationError(
                "Your review on this title is already exists",
            )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsStaffOrOwnerOrReadOnly]

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
