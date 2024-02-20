from django.urls import path, include
from api.views import home

urlpatterns = [
    path('', home, name='home'),
]