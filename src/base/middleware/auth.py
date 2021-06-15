from typing import List, Dict, Union, Tuple
import logging

from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import Group

import jwt
from rest_framework import status

from lunch_decision_maker.settings import SECRET_KEY
from user.models import User


logger = logging.getLogger('django')


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

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
                user_obj = User.objects.filter(username=payload.get('username')).first()
                if not user_obj:
                    return JsonResponse(data={
                        'message': 'user is not valid',
                        'success': False
                    }, status=status.HTTP_401_UNAUTHORIZED)
                setattr(request, 'user', user_obj)
                setattr(request, 'is_superuser', payload['is_superuser'])
            except Exception as err:
                return JsonResponse(data={
                    'message': f'auth exception {str(err)}',
                    'success': False,
                }, status=401)
        response = self.get_response(request)
        return response






