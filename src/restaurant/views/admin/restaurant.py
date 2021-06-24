from random import choices
from string import ascii_lowercase
import logging

from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    ListCreateAPIView,
    CreateAPIView,
)
from rest_framework.response import Response

from base.helpers import CustomPagination
from restaurant.models import Restaurant
from restaurant.serializers import (
    RestaurantSerializer
)
from user import permissions
from user.models import User
from user.serializers import UserLiteSerializer
from restaurant.helpers import slugify

logger = logging.getLogger('django')


class RestaurantListCreateAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsSuperUser]
    queryset = Restaurant.objects.filter()
    serializer_class = RestaurantSerializer
    pagination_class = CustomPagination
    ordering_fields = ['-created_at']

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name')
        is_active = self.request.query_params.get('is_active')
        if name:
            queryset = queryset.filter(name__istartswith=name)
        if is_active:
            queryset = queryset.filter(is_active=is_active)
        return queryset

    def perform_create(self, serializer):
        random_chars = ''.join(choices(ascii_lowercase, k=5))

        slug: str = slugify(self.request.data['name']) + '-' + random_chars
        serializer.save(
            created_by=UserLiteSerializer(self.request.user).data, slug=slug
        )


class RestaurantRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsSuperUser]
    queryset = Restaurant.objects.filter()
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'
    ordering_fields = ['-created_at']

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(RestaurantRetrieveUpdateAPIView, self).get_serializer(*args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super(RestaurantRetrieveUpdateAPIView, self).patch(
            request, *args, **kwargs
        )

    def perform_update(self, serializer):
        updated_by = UserLiteSerializer(self.request.user).data
        serializer.save(updated_by=updated_by)


class AssignOwner(CreateAPIView):
    permission_classes = [permissions.IsSuperUser]

    def post(self, request, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(slug=self.request.data['restaurant'])
            if restaurant.owner:
                return Response(
                    {
                        'success': False,
                        'message': 'Restaurant already has an owner'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            owner = self.request.data['owner']

            if not owner:
                return Response(
                    {
                        'success': False,
                        'message': 'You need to provide owner username',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if user already exists
            user = User.objects.filter(username=owner).first()
            if not user:
                return Response(
                    {
                        'success': False,
                        'message': 'Owner user is not exist in the system',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            restaurant_owner_group, created = Group.objects.get_or_create(
                name='RestaurantOwner'
            )
            restaurant_owner_group.user_set.add(user)
            restaurant.owner = user
            restaurant.save()

            return Response(
                {
                    'message': 'Owner successfully assigned'
                },
                status=status.HTTP_200_OK,
            )
        except (Restaurant.DoesNotExist, User.DoesNotExist) as e:
            return Response(
                {
                    'success': False,
                    'message': str(e),
                }, status=status.HTTP_404_NOT_FOUND,
            )
