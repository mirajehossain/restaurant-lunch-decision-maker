
from rest_framework import permissions
from rest_framework.generics import (
    RetrieveAPIView,
)
from restaurant.models import Restaurant
from restaurant.serializers import (
    RestaurantSerializer,
)


class RestaurantGetAPIView(RetrieveAPIView):
    permission_classes = (permissions.AllowAny)
    queryset = Restaurant.objects.filter()
    lookup_field = 'slug'
    serializer_class = RestaurantSerializer
