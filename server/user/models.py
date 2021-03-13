from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    # TODO use avatar from twitter/github
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    _role_choices = [
        'user',
        'owner',
        'admin',
    ]
    ROLE_CHOICES = zip(_role_choices, _role_choices)
    role = models.CharField(max_length=8, choices=ROLE_CHOICES)
