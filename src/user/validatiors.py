from typing import Dict
from rest_framework import status
from rest_framework.exceptions import ValidationError


def user_registration_validator(obj: Dict):
    if not obj.get('username'):
        raise ValidationError(
            {'detail': 'username can not be empty'}, code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    if not obj.get('first_name') or not obj.get('last_name'):
        raise ValidationError(
            {'detail': 'first_name, last_name can not be empty'}, code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    if not obj.get('password'):
        raise ValidationError(
            {'detail': 'password can not be empty'}, code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
