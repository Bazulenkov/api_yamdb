import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as VE
from django.core.mail import send_mail
from django.core.validators import validate_email
from rest_framework import viewsets, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


from .serializers import UserSerializer, UserForAdminSerializer
from .permissions import IsAdmin


User = get_user_model()


def get_confirmation_code():
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    confirmation_code =''
    for _ in range(10):
        confirmation_code += random.choice(chars)
    return confirmation_code


@api_view(['POST'])
@permission_classes([AllowAny])
def generate_confirmation_code(request):
    email = request.data.get('email')
    if email is None:
        raise ValidationError(
                {'email': 'This field is required'}
            )
    try:
        validate_email(email)
    except VE:
         raise ValidationError(
                 {'email': 'Enter a valid email address.'}
             )
    confirmation_code = get_confirmation_code()
    username = email.split('@')[0]
    # password = confirmation_code
    user = User.objects.filter(username=username).first()
    if not user:
        user = User.objects.create_user(
            username=username,
            email=email,
            #password=password,
        )
    user.confirmation_code=confirmation_code
    user.save()

    send_mail(
        'Письмо с кодом подтверждения для доступа на YamDB', 
        confirmation_code, 'admin@yamdb.fake', [email]
    )
    return Response({'email': email})


@api_view(['POST'])
@permission_classes([AllowAny])
def get_tokens_for_user(request):
    email = request.data.get('email')
    confirmation_code = request.data.get('confirmation_code')
    user = generics.get_object_or_404(User, email=email, confirmation_code=confirmation_code)
    refresh = RefreshToken.for_user(user)
    return Response (
        {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserForAdminSerializer
    permission_classes = [IsAuthenticated]#, IsAdmin]
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=username',]


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    