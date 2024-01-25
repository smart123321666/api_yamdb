from rest_framework.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Имя пользователя me не допустимо'
        )
    return value
