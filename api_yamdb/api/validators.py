import datetime

from rest_framework.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Имя пользователя me не допустимо'
        )
    return value


def validate_year(value):
    current_year = datetime.datetime.now().year
    if value > current_year:
        raise ValidationError("Год не может быть больше текущего года.")
