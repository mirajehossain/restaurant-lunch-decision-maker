import logging
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from base.helpers import CustomPagination
from user.models import User
from user.permissions import IsSuperUser
from user.serializers import UserLiteSerializer
from user.validatiors import user_registration_validator

logger = logging.getLogger('django')


class CreateAdminAPIView(CreateAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_registration_validator(request.data)

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = request.data.get('username')
        is_superuser = request.data.get('is_superuser')

        check_user = User.objects.filter(username=request.data.get('username')).first()
        if check_user:
            return Response({
                'message': 'User is already registered'
            }, status=status.HTTP_409_CONFLICT)

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_superuser=True if is_superuser is True else False,
        )
        user.set_password(request.data.get('password'))
        user.save()

        return Response({
            'message': 'Successfully registered new admin',
            'data': UserLiteSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class CreateUserAPIView(CreateAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_registration_validator(request.data)

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = request.data.get('username')
        address = request.data.get('address')
        gender = request.data.get('gender')

        check_user = User.objects.filter(username=request.data.get('username')).first()
        if check_user:
            return Response({
                'message': 'User is already registered'
            }, status=status.HTTP_409_CONFLICT)

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        if address:
            user.address = address
        if gender:
            user.gender = gender

        user.set_password(request.data.get('password'))
        user.save()

        return Response({
            'message': 'Successfully registered new user',
            'data': UserLiteSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class UserListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = UserLiteSerializer
    queryset = User.objects.filter()
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')

