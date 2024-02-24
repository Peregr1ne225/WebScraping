from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from api import views


router = routers.DefaultRouter()
router.register(r'product', views.ProductViewset)
router.register(r'brand', views.BrandViewset)
router.register(r'category', views.CategoryViewset)
router.register(r'retail', views.RetailerViewset)
router.register(r'log', views.LogViewset)
router.register(r'brand_top', views.BrandTopViewset)
router.register(r'category_top', views.CategoryTopViewset)
router.register(r'category_parent', views.CategoryParentViewset)
router.register(r'category_root', views.CategoryRootViewset)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

urlpatterns += router.urls
