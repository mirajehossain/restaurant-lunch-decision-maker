from django.urls import path

from restaurant.views import (
    RestaurantListCreateAPIView,
    RestaurantRetrieveUpdateAPIView,
    AssignOwner,
)

app_name = 'admin_restaurant'

urlpatterns = [
    path(
        'restaurant',
        RestaurantListCreateAPIView.as_view(),
        name='v1-admin-create-restaurant',
    ),
    path(
        'restaurant/<str:slug>',
        RestaurantRetrieveUpdateAPIView.as_view(),
        name='v1-admin-get-update-restaurant',
    ),
    path(
        'assign-owner',
        AssignOwner.as_view(),
        name='v1-admin-assign-restaurant-owner',
    ),
]
