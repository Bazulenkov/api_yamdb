from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

router = DefaultRouter()
router.register("users", views.UserViewSet)
router.register("titles", views.TitleViewset)
router.register("categories", views.CategoryViewSet)
router.register("genres", views.GenryViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    views.ReviewViewSet,
    basename="reviews",
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    views.CommentViewSet,
    basename="comments",
)


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
]
