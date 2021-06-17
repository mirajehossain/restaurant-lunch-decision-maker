from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from user import permissions
from user.serializers import UserLiteSerializer
from restaurant.models import Restaurant
from item.models import Item, MenuHours
from item.serializers import (
    ItemSerializer,
    MenuHoursSerializer,
    ItemLiteSerializer,
)


class ItemsListCreateAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsSuperUser | permissions.IsRestaurantOwner]
    queryset = Item.objects.all()
    serializer_class = ItemLiteSerializer

    def get_queryset(self):
        if self.request.query_params.get('restaurant_slug'):
            try:
                restaurant = Restaurant.objects.get(
                    slug=self.request.query_params.get('restaurant_slug')
                )
                return Item.objects.filter(restaurant=restaurant)
            except Restaurant.DoesNotExist:
                return []
        return super(ItemsListCreateAPIView, self).get_queryset()

    def create(self, request, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(
                slug=request.data.get('restaurant_slug')
            )
        except Restaurant.DoesNotExist:
            return Response(
                {'success': False, 'message': 'Restaurant does not exist'},
                status=status.HTTP_404_NOT_FOUND,
            )
        menu_hours = request.data.get('menu_hours')

        menu_hours_list = []
        if menu_hours:
            for menu in menu_hours:
                add = MenuHours.objects.get(pk=menu)
                menu_hours_list.append(add)

        request.data['restaurant'] = restaurant
        request.data['menu_hours'] = menu_hours_list
        return super(ItemsListCreateAPIView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            created_by=UserLiteSerializer(self.request.user).data,
            restaurant=self.request.data['restaurant'],
            menu_hours=self.request.data['menu_hours'],
        )


class ItemRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsSuperUser | permissions.IsRestaurantOwner]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

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
        new_menu_hours = request.data.get('menu_hours')

        if new_menu_hours:
            existing_menu_hours_map = {}
            existing_menu_hour_ids = []
            existing_menu_hours = item.menu_hours.all()
            for existing_menu_hour in existing_menu_hours:
                existing_menu_hours_map[existing_menu_hour.id] = existing_menu_hour
                existing_menu_hour_ids.append(existing_menu_hour.id)

            new_menu_hours_object = list(MenuHours.objects.filter(id__in=new_menu_hours))

            item.menu_hours.add(*new_menu_hours_object)

            deleted_menu_hour_ids = set(existing_menu_hour_ids).difference(new_menu_hours)
            deleted_menu_hours_object = list(MenuHours.objects.filter(id__in=deleted_menu_hour_ids))
            item.menu_hours.remove(*deleted_menu_hours_object)

            request.data['menu_hours'] = new_menu_hours_object

        return super(ItemRetrieveUpdateAPIView, self).update(request, *args, **kwargs)

    def perform_update(self, serializer):
        return serializer.save(
            updated_by=UserLiteSerializer(self.request.user).data, **self.request.data
        )


class MenuHoursListCreateAPIView(ListCreateAPIView):
    serializer_class = MenuHoursSerializer
    queryset = MenuHours.objects.all()
    permission_classes = [IsAuthenticated, permissions.IsSuperUser | permissions.IsRestaurantOwner]

    def get_queryset(self):
        if self.request.query_params.get('restaurant_slug'):
            try:
                return MenuHours.objects\
                    .filter(restaurant__slug=self.request.query_params.get('restaurant_slug'))\
                    .order_by('id')
            except Restaurant.DoesNotExist:
                return []

        return super(MenuHoursListCreateAPIView, self).get_queryset()

    def create(self, request, *args, **kwargs):
        return super(MenuHoursListCreateAPIView, self).create(
            request, *args, **kwargs
        )

    def perform_create(self, serializer):
        serializer.save(
            created_by=UserLiteSerializer(self.request.user).data,
            updated_by=UserLiteSerializer(self.request.user).data,
            item=self.request.data.get('item'),
        )


class MenuHoursRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = MenuHours.objects.all()
    serializer_class = MenuHoursSerializer
    permission_classes = [permissions.IsSuperUser | permissions.IsRestaurantOwner]

    def get(self, request, *args, **kwargs):
        menu = self.get_object()
        serializer = MenuHoursSerializer(menu)
        return Response(
            {'success': True, 'data': serializer.data}, status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        return super(MenuHoursRetrieveUpdateDestroyAPIView, self).update(request, *args, **kwargs)

    def perform_update(self, serializer):
        return serializer.save(
            updated_by=UserLiteSerializer(self.request.user).data, **self.request.data
        )
