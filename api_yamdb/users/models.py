from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api.validators import validate_username


class CustomUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    email = models.EmailField(
        'email',
        unique=True,)
    role = models.CharField('Роль', max_length=settings.MAX_ROLE_LENGTH,
                            choices=ROLE_CHOICES,
                            default=USER)
    bio = models.TextField('Биография', blank=True)

    username = models.CharField(
        'username',
        max_length=settings.MAX_USERNAME_LENGTH,
        unique=True,
        validators=[UnicodeUsernameValidator(), validate_username]
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_admin
