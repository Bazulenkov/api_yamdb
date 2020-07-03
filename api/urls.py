from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


router = routers.DefaultRouter()
router.register("users", views.UserViewSet)
router.register("titles", views.TitleViewset)


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
    path("categories/", views.CategoriesList.as_view(), name="list_categories"),
    path("categories/<slug>/", views.CategoryDestroy.as_view(), name="destroy_category"),
    path("genres/", views.GenresList.as_view(), name="list_genres"),
    path("genres/<slug>/", views.GenreDestroy.as_view(), name="destroy_genre"),
    path("", include(router.urls)),
]
