import uuid
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError


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
    role = models.CharField('Роль', max_length=100,
                            choices=ROLE_CHOICES,
                            default=USER)
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(max_length=70,
                                         unique=True,
                                         blank=True,
                                         null=True,
                                         default=uuid.uuid4)
    def validate_not_me(value):
        if value.lower() == 'me':
            raise ValidationError('The nickname "me" is not allowed.', code='invalid_nickname')
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator(),]
    )


    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_admin
