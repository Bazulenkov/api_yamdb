from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    # following = serializers.ReadOnlyField(source='following.username')

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User
