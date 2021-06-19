import datetime
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from item.serializers import ItemSerializer
from item.models import Item


class ItemsListView(ListAPIView):
    permission_classes = (IsAuthenticated, permissions.AllowAny,)
    queryset = Item.objects.filter(status='active')

    date = datetime.datetime.now().date()
    year, month, day = str(date).split('-')
    day_name = datetime.date(int(year), int(month), int(day))
    week_day = day_name.strftime("%A").lower()

    queryset = queryset.filter(menu_hours__week_day=week_day)

    serializer_class = ItemSerializer
