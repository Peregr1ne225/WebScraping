from django.shortcuts import render

# Create your views here.
from .models import *
from .serializers import *
from rest_framework import permissions, viewsets

class ProductViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        ProductID = self.request.query_params.get('ProductID')
        if ProductID:
            queryset = queryset.filter(ProductID=ProductID)
        return queryset
    
class BrandViewset(viewsets.ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RetailerViewset(viewsets.ModelViewSet):
    queryset = Retailers.objects.all()
    serializer_class = RetailerSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LogViewset(viewsets.ModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]