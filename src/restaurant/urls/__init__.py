from django.urls import path, include

app_name = 'restaurant'

urlpatterns = [
    path('admin/', include('restaurant.urls.admin', namespace='admin_restaurant_api')),
    path('users/', include('restaurant.urls.users', namespace='users_restaurant_api')),
    path('merchant/', include('restaurant.urls.merchant', namespace='merchant_restaurant_api')),
]
