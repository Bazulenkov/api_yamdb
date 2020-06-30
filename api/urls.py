from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from . import views


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
# router.register(r'posts/(?P<post_id>\d+)/comments', views.CommentViewSet)


urlpatterns = [
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/', views.get_tokens_for_user, name='token_obtain_pair'),
    path('auth/email/', views.generate_confirmation_code, name='generate_confirmation_code'),
    # path('follow/', views.FollowAPIView.as_view(), name='follow'),
    # path('group/', views.GroupAPIView.as_view(), name='group'),
    path('', include(router.urls)),
]
