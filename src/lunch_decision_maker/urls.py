"""lunch_decision_maker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from lunch_decision_maker.views import HealthCheckAPI

v1_patterns = [
    path('users/', include('user.urls', namespace='user_api')),
    path('restaurants/', include('restaurant.urls', namespace='restaurant_api')),
    path('items/', include('item.urls', namespace='restaurant_item_api')),
    path('votes/', include('voting.urls', namespace='restaurant_votes_api')),
]

urlpatterns = [
    path('', HealthCheckAPI.as_view()),
    path('api/', include([
        path('v1.0.0/', include(v1_patterns))
    ])),
]
