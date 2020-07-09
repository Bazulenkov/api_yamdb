from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRoles:
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    choices = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )


class YamUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=9, choices=UserRoles.choices, default=UserRoles.USER
    )
