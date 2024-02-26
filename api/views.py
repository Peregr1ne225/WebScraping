from django.shortcuts import render
from .savenewscore import check_update

# Create your views here.
#from django.http import HttpResponse
from .models import *
from .serializers import *
from rest_framework import permissions, viewsets
from rest_framework import pagination, status, exceptions
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
        search = self.request.query_params.get('search')
        
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
        if search:
            queryset = queryset.filter(ProductName__icontains=search)
        return queryset

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            for field, value in request.data.items():
                if field == 'BrandID':
                    value = Brands.objects.get(BrandID=value)
                if field == 'RetailID':
                    value = Retailers.objects.get(RetailID=value)
                if field == 'CategoryID':
                    value = Categories.objects.get(CategoryID=value)
                setattr(instance, field, value)
            if ('ProductName' in request.data) and ('ProductID' in request.data):
                sim_group, sim_score = check_update(instance.ProductID, request.data['ProductName'])
                print("sim_group: ", sim_group, "sim_score: ", sim_score)
                if sim_group is not None:
                    instance.SimilarGroup = sim_group
                    instance.SimilarScore = sim_score
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
    search = request.GET.get('search')

    if search:
        url = f'http://127.0.0.1:8000/api/product/?search={search}'
        template = 'search.html'
        if brand:
            url = url + f'&brand={brand}'
    elif brand:
        url = f'http://127.0.0.1:8000/api/product/?brand={brand}'
        template = 'index.html'
    else:
        url = 'http://127.0.0.1:8000/api/product/'
        template = 'index.html'
    
    response = requests.get(url)
    data = response.json()
    data = data['results']
    return render(request, template, {'data': json.dumps(data)})

def cate(request, id):
    brand = request.GET.get('brand')
    search = request.GET.get('search')
    results = []

    if search:
        url = f'http://127.0.0.1:8000/api/product/?search={search}&category={str(id)}'
        if brand:
            url = url + f'&brand={brand}'
        template = 'search.html'
    elif brand:
        url = 'http://127.0.0.1:8000/api/product/?category='+str(id)+'&brand='+brand
        template = 'cate.html'
    else:
        url = 'http://127.0.0.1:8000/api/product/?category=' + str(id)
        template = 'cate.html'
    
    while url:
        response = requests.get(url)
        data = response.json()
        results.extend(data['results'])
        url = data['next'] if 'next' in data else None

    return render(request, template, {'data': json.dumps(results)})
