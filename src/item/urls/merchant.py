from django.urls import path

from item.views import (
    MerchantItemsListCreateAPIView,
    MerchantItemRetrieveUpdateAPIView,
)


app_name = 'merchant_item'


urlpatterns = [
    path('items', MerchantItemsListCreateAPIView.as_view(), name='v1-merchant-item-list-create'),
    path(
        'items/<int:pk>',
        MerchantItemRetrieveUpdateAPIView.as_view(),
        name='v1-admin-item-retrieve-update',
    ),
]
