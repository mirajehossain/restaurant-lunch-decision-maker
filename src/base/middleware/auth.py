import random
from typing import List, Dict, Union, Tuple
import logging

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import Group

import jwt

from lunch_decision_maker.settings import SECRET_KEY
from user.models import User


logger = logging.getLogger('django')


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def get_user(data: Dict) -> Union[Tuple[User, List[Group]], object]:
        try:
            user, created = User.objects.get_or_create(username=data.get('username'))

            if created:
                user.is_superuser = data.get('is_superuser')
                user.first_name = data.get('first_name')
                user.last_name = data.get('last_name')
                user.is_staff = data.get('is_staff')
                user.is_active = data.get('is_active')
                user.email = data.get('email')
                user.is_new = True
                if data.get('groups'):
                    for group in data.get('groups'):
                        group_obj, _ = Group.objects.get_or_create(name=group)
                        group_obj.user_set.add(user)
                user.save()
            return user, user.groups
        except Exception as err:
            logger.error(f'error creating or retrieving user. reason: {err}')
            return

    def __call__(self, request: HttpRequest):
        setattr(request, '_dont_enforce_csrf_checks', True)
        auth_header: str = request.headers.get('authorization')
        if auth_header:
            token_obj: List[str] = auth_header.split(' ')
            if token_obj[0].lower() != 'bearer':
                return JsonResponse(data={
                        'message': 'invalid token type',
                        'success': False,
                    }, status=400)
            try:
                payload: Dict = jwt.decode(jwt=token_obj[1], key=SECRET_KEY, algorithms='HS256', verify=True)
                if payload['token_type'] != 'access':
                    return JsonResponse(data={
                        'message': 'no access token provided',
                        'success': False
                    }, status=400)
                user_obj, groups = self.get_user(data=payload)
                if not user_obj:
                    return JsonResponse(data={
                        'message': 'cannot retrieve user information',
                        'success': False
                    }, status=401)
                setattr(request, 'user', user_obj)
                setattr(request, 'groups', payload['groups'])
                setattr(request, 'is_superuser', payload['is_superuser'])
            except Exception as err:
                return JsonResponse(data={
                    'message': f'auth exception {str(err)}',
                    'success': False,
                }, status=401)
        response = self.get_response(request)
        return response






