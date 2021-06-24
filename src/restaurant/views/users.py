
from rest_framework import permissions, status
from rest_framework.generics import (
    RetrieveAPIView,
)
from rest_framework.response import Response

from restaurant.models import Restaurant
from restaurant.serializers import (
    RestaurantSerializer,
)


class RestaurantGetAPIView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            slug = kwargs.get('slug')
            restaurant = Restaurant.objects.get(slug=slug)

            return Response({
                'success': True,
                'message': 'restaurant details',
                'data': RestaurantSerializer(restaurant).data
            }, status=status.HTTP_200_OK)

        except Restaurant.DoesNotExist:
            return Response({
                'success': False,
                'message': 'restaurant does not found',
            }, status=status.HTTP_400_BAD_REQUEST)
