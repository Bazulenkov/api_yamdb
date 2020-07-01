from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserForAdminSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class UserSerializer(UserForAdminSerializer):
    role = serializers.CharField(read_only=True)
    