from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class YamUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=9, choices=ROLE, default='user')
    confirmation_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        pass
