from rest_framework import serializers
from .models import *

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

class RecursionSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        serializers = self.parent.parent.__class__(value, context=self.context)
        return serializers.data

class CategoryParentSerializer(serializers.ModelSerializer):
    child_categories = RecursionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Categories
        fields = ['CategoryID', 'CategoryName', 'CategoryScore','ParentCategoryID', 'child_categories']
        #fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['CategoryID', 'CategoryName', 'CategoryScore', 'ParentCategoryID']


class ProductSerializer(serializers.ModelSerializer):
    BrandName = serializers.SlugRelatedField(source='BrandID', read_only=True, slug_field='BrandName')
    RetailName = serializers.SlugRelatedField(source='RetailID', read_only=True, slug_field='Retail')
    Price = serializers.FloatField()
    class Meta:
        model = Products
        fields = ('ProductID', 'ProductName', 'BrandID', 'BrandName',
                  'Price', 'Stock', 'Description', 'URL', 'PicURL', 
                  'CategoryID', 'RetailID', 'RetailName', 'DateEdit', 
                  'SimilarGroup', 'SimilarScore', 'DateCreate')
        #fields = ('ProductName', 'Price', 'Stock', 'Description', 'SimilarGroup', 'SimilarScore')
        
