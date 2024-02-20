from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import *
from .serializers import *
from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from django.template import loader

class ProductViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        id = self.request.query_params.get('id')
        group = self.request.query_params.get('group')
        retail = self.request.query_params.get('retail')
        if id:
            queryset = queryset.filter(ProductID=id)
        if group:
            queryset = queryset.filter(SimilarGroup=group)
        if retail:
            queryset = queryset.filter(RetailID=retail)
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

def FirstView(request):
    template = loader.get_template('first.html')
    return HttpResponse(template.render())