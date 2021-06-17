from django.urls import path, include

app_name = 'items'

urlpatterns = [
    path('admin/', include('item.urls.admin', namespace='admin_restaurant_api')),
    path('users/', include('item.urls.users', namespace='users_restaurant_api')),
    path('merchant/', include('item.urls.merchant', namespace='merchant_restaurant_api')),
]
