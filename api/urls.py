from django.urls import path
from api.views import FirstView

urlpatterns = [
    path('', FirstView, name='first'),
]