from django.urls import path, include
from api.views import home, cate, dashboard, check_status

urlpatterns = [
    path('', home, name='home'),
    path('<int:id>/', cate, name='cate'),
    path('dashboard/', dashboard, name='dashboard'),
    path('check_status/', check_status, name='check_status')
]