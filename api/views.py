from django.urls import reverse
from django.shortcuts import render

# Create your views here.
#from django.http import HttpResponse
from .models import *
from .serializers import *
from rest_framework import permissions, viewsets
from rest_framework import pagination
from rest_framework.authentication import TokenAuthentication
import requests
import json

class NoLimitPagination(pagination.PageNumberPagination):
    page_size = None

class ProductViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        id = self.request.query_params.get('id')
        group = self.request.query_params.get('group')
        retail = self.request.query_params.get('retail')
        category = self.request.query_params.get('category')
        if id:
            queryset = queryset.filter(ProductID=id)
        if group:
            queryset = queryset.filter(SimilarGroup=group)
        if retail:
            queryset = queryset.filter(RetailID=retail)
        if category:
            category_ids = get_descendant_category_ids(category)
            queryset = queryset.filter(CategoryID__in=category_ids)
        return queryset
    
class BrandViewset(viewsets.ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializer
    pagination_class = NoLimitPagination
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    pagination_class = NoLimitPagination
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = super().get_queryset()
        parent = self.request.query_params.get('parent')
        if parent is None:
            queryset = queryset.filter(ParentCategoryID=None)
        elif parent:
            queryset = queryset.filter(ParentCategoryID=parent)
        return queryset

class RetailerViewset(viewsets.ModelViewSet):
    queryset = Retailers.objects.all()
    serializer_class = RetailerSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LogViewset(viewsets.ModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

def get_descendant_category_ids(CategoryID):
    descendant_ids = set()
    stack = [CategoryID]
    while stack:
        current_id = stack.pop()
        descendant_ids.add(current_id)
        child_ids = Categories.objects.filter(ParentCategoryID=current_id).values_list('CategoryID', flat=True)
        stack.extend(child_ids)
    return list(descendant_ids)

def home(request):
    response = requests.get('http://127.0.0.1:8000/api/product/')
    data = response.json()
    data = data['results']
    #print(data)
    return render(request, 'index.html', {'data': data})

def cate(request, id):
    response = requests.get('http://127.0.0.1:8000/api/product/?category='+str(id))
    data = response.json()
    data = data['results']
    return render(request, 'cate.html', {'data': json.dumps(data)})