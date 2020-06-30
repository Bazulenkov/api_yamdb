from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from . import views


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)


urlpatterns = [
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/', views.get_tokens_for_user, name='token_obtain_pair'),
    path('auth/email/', views.generate_confirmation_code, name='generate_confirmation_code'),
    path('users/me/', views.UserRetrieveUpdateAPIView.as_view(), name='me'),
    path('', include(router.urls)),
]
