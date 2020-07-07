from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView

from . import views


router = DefaultRouter()
router.register("users", views.UserViewSet)
router.register("titles", views.TitleViewSet)
router.register("categories", views.CategoriesViewSet)
router.register("genres", views.GenresViewSet)
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
    path("auth/token/", views.get_tokens_for_user, name="get_tokens_for_user"),
    path(
        "auth/email/",
        views.generate_confirmation_code,
        name="generate_confirmation_code",
    ),
    path("", include(router.urls)),
]
