from rest_framework.generics import (
    RetrieveUpdateAPIView,
    ListAPIView,
)
from restaurant.models import Restaurant
from restaurant.serializers import (
    RestaurantSerializer,
)
from user import permissions
from user.serializers import UserLiteSerializer


class RestaurantMerchantListAPIView(ListAPIView):
    permission_classes = [permissions.IsRestaurantOwner]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    ordering_fields = ['-created_at']

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)


class RestaurantMerchantRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsRestaurantOwner]
    queryset = Restaurant.objects.filter()
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'
    ordering_fields = ['-created_at']

    def get_object(self):
        return Restaurant.objects.get(
            owner=self.request.user, slug=self.kwargs.get('slug')
        )
