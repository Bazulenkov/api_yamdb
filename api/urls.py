<<<<<<< HEAD
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


router = routers.DefaultRouter()
router.register("users", views.UserViewSet)


urlpatterns = [
    path(
        "auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("auth/token/", views.get_tokens_for_user, name="token_obtain_pair"),
    path(
        "auth/email/",
        views.generate_confirmation_code,
        name="generate_confirmation_code",
    ),
    path("users/me/", views.UserRetrieveUpdateAPIView.as_view(), name="me"),
    path("", include(router.urls)),
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitleViewset, GenresList, GenreDestroy, CategoriesList, CategoryDestroy

router = DefaultRouter()
router.register("titles", TitleViewset)


urlpatterns = [
    path('', include(router.urls)),
    path("categories/", CategoriesList.as_view(), name="list_categories"),
    path("categories/<slug>/", CategoryDestroy.as_view(), name="destroy_category"),
    path("genres/", GenresList.as_view(), name="list_genres"),
    path("genres/<slug>/", GenreDestroy.as_view(), name="destroy_genre"),
>>>>>>> develop/titles-categories-genres/konstantin
]
