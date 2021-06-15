from django.urls import path
from user.views import HelloWorldAPIView, CreateAdminAPIView, CreateUserAPIView

app_name = 'user'

urlpatterns = [
    path('hello', HelloWorldAPIView.as_view(), name='hello-world'),
    path('register-admin', CreateAdminAPIView.as_view(), name='create-admin'),
    path('register-user', CreateUserAPIView.as_view(), name='create-user'),
]
