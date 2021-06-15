from django.urls import path
from user.views import CreateAdminAPIView, CreateUserAPIView, UserListAPIView

app_name = 'user'

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('register-admin', CreateAdminAPIView.as_view(), name='create-admin'),
    path('register-user', CreateUserAPIView.as_view(), name='create-user'),
]
