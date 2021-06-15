from django.urls import path
from user.views import HelloWorldAPIView

app_name = 'user'

urlpatterns = [
    path('hello', HelloWorldAPIView.as_view(), name='hello-world'),
]
