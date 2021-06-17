from django.urls import path

from item.views import ItemsListView

app_name = 'user_item'

urlpatterns = [
    path('items', ItemsListView.as_view(), name='api-v1-public-item-list'),
]
