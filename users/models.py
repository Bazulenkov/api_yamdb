from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE = (
    ('u', 'user'),
    ('m', 'moderator'),
    ('a', 'admin'),
)


class YamUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=1, choices=ROLE, default='u')
    confirmation_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        pass
