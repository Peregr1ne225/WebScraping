from django.urls import reverse
from django.shortcuts import render

# Create your views here.
#from django.http import HttpResponse
from .models import *
from .serializers import *
from rest_framework import permissions, viewsets
from rest_framework import pagination, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
import requests
import json

class NoLimitPagination(pagination.PageNumberPagination):
    page_size = None

class ProductViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    #pagination_class = NoLimitPagination
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        id = self.request.query_params.get('id')
        group = self.request.query_params.get('group')
        retail = self.request.query_params.get('retail')
        category = self.request.query_params.get('category')
        brand = self.request.query_params.get('brand')
        name = self.request.query_params.get('name')
        if id:
            queryset = queryset.filter(ProductID=id)
        if group:
            queryset = queryset.filter(SimilarGroup=group)
        if retail:
            queryset = queryset.filter(RetailID=retail)
        if category:
            category_ids = get_descendant_category_ids(category)
            queryset = queryset.filter(CategoryID__in=category_ids)
        if brand:
            queryset = queryset.filter(BrandID=brand)
        if name:
            queryset = queryset.filter(ProductName__icontains=name)
        return queryset
    
class BrandViewset(viewsets.ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializer
    pagination_class = NoLimitPagination
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = super().get_queryset()
        id = self.request.query_params.get('id')
        if id:
            queryset = queryset.filter(BrandID=id)
        return queryset
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.BrandScore += 1
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BrandTopViewset(viewsets.ModelViewSet):
    queryset = Brands.objects.all().order_by('-BrandScore')[:10]
    serializer_class = BrandSerializer

class CategoryTopViewset(viewsets.ModelViewSet):
    queryset = Categories.objects.filter(ParentCategoryID__isnull=True).order_by('-CategoryScore')[:10]
    serializer_class = CategorySerializer

class CategoryParentViewset(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoryParentSerializer
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

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.CategoryScore += 1
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

def get_top_category(category):
    if category.ParentCategoryID is None:
        return category
    else:
        return get_top_category(category.ParentCategoryID)

class CategoryRootViewset(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        if id is not None:
            category = self.queryset.get(CategoryID=id)
            root_category = get_top_category(category)
            return Response({'root_category_id': root_category.CategoryID})
        else:
            return Response({"error": "No id provided"}, status=status.HTTP_400_BAD_REQUEST)

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
    brand = request.GET.get('brand')
    print(brand)
    if brand:
        response = requests.get('http://127.0.0.1:8000/api/product/?brand='+brand)
    else:
        response = requests.get('http://127.0.0.1:8000/api/product/')
    data = response.json()
    data = data['results']
    return render(request, 'index.html', {'data': json.dumps(data)})

def cate(request, id):
    url = 'http://127.0.0.1:8000/api/product/?category=' + str(id)
    results = []

    while url:
        response = requests.get(url)
        data = response.json()
        results.extend(data['results'])

        url = data['next'] if 'next' in data else None

    return render(request, 'cate.html', {'data': json.dumps(results)})