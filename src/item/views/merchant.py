from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from user import permissions
from user.serializers import UserLiteSerializer
from restaurant.models import Restaurant
from item.models import Item
from item.serializers import (
    ItemSerializer,
)


class MerchantItemsListCreateAPIView(ListCreateAPIView):
    permission_classes = [
        permissions.IsRestaurantOwner
    ]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        if self.request.query_params.get('restaurant_slug'):
            try:
                restaurant = Restaurant.objects.get(
                    slug=self.request.query_params.get('restaurant_slug'),
                    owner=self.request.user
                )
                return Item.objects.filter(restaurant=restaurant)
            except Restaurant.DoesNotExist:
                return []
        return super(MerchantItemsListCreateAPIView, self).get_queryset()

    def create(self, request, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(
                slug=request.data.get('restaurant_slug'),
                owner=self.request.user
            )
        except Restaurant.DoesNotExist:
            return Response(
                {'success': False, 'message': 'Restaurant does not exist'},
                status=status.HTTP_404_NOT_FOUND,
            )

        request.data['restaurant'] = restaurant
        return super(MerchantItemsListCreateAPIView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            created_by=UserLiteSerializer(self.request.user).data,
            restaurant=self.request.data['restaurant'],
            status='inactive'
        )


class MerchantItemRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [
        permissions.IsRestaurantOwner
    ]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(restaurant__owner=self.request.user)

    def get_object(self):
        return Item.objects.get(restaurant__owner=self.request.user, id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        item = self.get_object()
        serializer = ItemSerializer(item)
        return Response(
            {'success': True, 'data': serializer.data}, status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        item = self.get_object()
        if request.data.get('restaurant'):
            try:
                restaurant = Restaurant.objects.get(pk=request.data.get('restaurant'))
                item.restaurant = restaurant
                request.data['restaurant'] = restaurant
            except Restaurant.DoesNotExist:
                return Response(
                    {'success': False, 'message': 'Restaurant does not exist'},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return super(MerchantItemRetrieveUpdateAPIView, self).update(request, *args, **kwargs)

    def perform_update(self, serializer):
        return serializer.save(
            updated_by=UserLiteSerializer(self.request.user).data, **self.request.data
        )
