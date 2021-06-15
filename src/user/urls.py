from django.urls import path
from user.views import HelloWorldAPIView, CreateAdminAPIView

app_name = 'user'

urlpatterns = [
    path('hello', HelloWorldAPIView.as_view(), name='hello-world'),
    path('register-admin', CreateAdminAPIView.as_view(), name='create-admin'),
]
