from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from api import views


router = routers.DefaultRouter()
router.register(r'product', views.ProductViewset, basename='product')
router.register(r'brand', views.BrandViewset, basename='brand')
router.register(r'category', views.CategoryViewset, basename='category')
router.register(r'retail', views.RetailerViewset, basename='retail')
router.register(r'log', views.LogViewset, basename='log')
router.register(r'brand_top', views.BrandTopViewset, basename='top_brand')
router.register(r'category_top', views.CategoryTopViewset, basename='top_category')
router.register(r'category_parent', views.CategoryParentViewset, basename='category_parent')
router.register(r'category_root', views.CategoryRootViewset, basename='category_root')
router.register(r'update', views.UpdateViewset, basename='update')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

#urlpatterns += router.urls
