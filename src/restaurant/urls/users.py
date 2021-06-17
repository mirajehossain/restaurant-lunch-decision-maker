from django.urls import path

from restaurant.views import (
    RestaurantGetAPIView,
)

app_name = 'user_restaurant'

urlpatterns = [
    path('restaurant/<str:slug>', RestaurantGetAPIView.as_view(), name='v1-restaurant-get-api-view'),
]
