from django.urls import path

from restaurant.views import (
    RestaurantMerchantListAPIView,
    RestaurantMerchantRetrieveUpdateAPIView,
)


app_name = 'merchant_restaurant'

urlpatterns = [
    path(
        'restaurant',
        RestaurantMerchantListAPIView.as_view(),
        name='v1-merchant-list-restaurant',
    ),
    path(
        'restaurant/<str:slug>',
        RestaurantMerchantRetrieveUpdateAPIView.as_view(),
        name='v1-merchant-get-update-restaurant',
    ),
]
