from django.urls import path

from item.views import (
    ItemsListCreateAPIView,
    ItemRetrieveUpdateAPIView,
    MenuHoursRetrieveUpdateDestroyAPIView,
    MenuHoursListCreateAPIView
)

app_name = 'admin_item'

urlpatterns = [
    path('items', ItemsListCreateAPIView.as_view(), name='v1-admin-item-list-create'),
    path(
        'items/<int:pk>',
        ItemRetrieveUpdateAPIView.as_view(),
        name='v1-admin-item-retrieve-update',
    ),
    path(
        'menu-hours',
        MenuHoursListCreateAPIView.as_view(),
        name='v1-admin-menu-hours-list-create',
    ),
    path(
        'menu-hours/<int:pk>',
        MenuHoursRetrieveUpdateDestroyAPIView.as_view(),
        name='v1-admin-menu-hours-retrieve-update',
    ),
]
