from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('ProductID', 'ProductName', 'BrandID', 'Price', 'Stock', 
                  'Description', 'URL', 'PicURL', 'CategoryID', 'RetailID',
                  'DateEdit', 'SimilarGroup', 'SimilarScore', 'DateCreate')
        #fields = ('ProductName', 'Price', 'Stock', 'Description', 'SimilarGroup', 'SimilarScore')
        
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = '__all__'

class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailers
        fields = '__all__'

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'