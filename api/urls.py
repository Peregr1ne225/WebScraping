from django.urls import path, include
from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r'product', views.ProductViewset)
router.register(r'brand', views.BrandViewset)
router.register(r'category', views.CategoryViewset)
router.register(r'retail', views.RetailerViewset)
router.register(r'log', views.LogViewset)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += router.urls
