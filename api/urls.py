from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews")
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/", basename="comments"
)

urlpatterns = [path("", include(router.urls))]
