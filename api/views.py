<<<<<<< HEAD
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as VE
from django.core.mail import send_mail
from django.core.validators import validate_email
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from .serializers import UserForAdminSerializer, UserSerializer


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
=======
from rest_framework import generics, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .filters import TitleFilter
from .models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoriesList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["=name", ]


class CategoryDestroy(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class GenresList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["=name", ]


class GenreDestroy(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    filter_backends = [DjangoFilterBackend, ]
    ordering_fields = ["name"]

    def perform_create(self, serializer):
        category = generics.get_object_or_404(Category, slug=self.request.data.get("category"))
        genre = Genre.objects.filter(slug__in=self.request.data.getlist("genre"))
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        title = self.get_object()
        category = generics.get_object_or_404(Category, slug=self.request.data.get("category"))
        genre = Genre.objects.filter(slug__in=self.request.data.getlist("genre"))
        title.genre.set(genre)
        serializer.save()
        title.category = category
        #title.save()
        #serializer.save()
>>>>>>> develop/titles-categories-genres/konstantin
