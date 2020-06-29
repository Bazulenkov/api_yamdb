import random

from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


User = get_user_model()


def get_confirmation_code():
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    confirmation_code =''
    for i in range(10):
        confirmation_code += random.choice(chars)
    return confirmation_code


@api_view(['POST'])
def generate_confirmation_code(request):
    email = request.data.get('email')
    if email is None:
        raise ValidationError(
                {'email': 'This field is required'}
            )

    confirmation_code = get_confirmation_code()
    username = email.split('@')[0]
    password = confirmation_code
    # User.objects.filter(username=username).exist
    User.objects.create_user(
        username=username,
        email=email,
        password=password,
        confirmation_code=confirmation_code
    )

    send_mail(
        'Письмо с кодом подтверждения для доступа на YamDB', 
        confirmation_code, 'admin@yamdb.fake', [email]
    )
    return Response({"email": email})