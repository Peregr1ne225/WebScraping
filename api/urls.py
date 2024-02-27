from django.urls import path, include
from api.views import home, cate, dashboard

urlpatterns = [
    path('', home, name='home'),
    path('<int:id>/', cate, name='cate'),
    path('dashboard/', dashboard, name='dashboard'),
]