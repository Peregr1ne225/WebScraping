from django.shortcuts import render

# Create your views here.
from .models import *
from .serializers import ProductSerializer
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