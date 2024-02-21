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

class RecursionSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        serializers = self.parent.parent.__class__(value, context=self.context)
        return serializers.data

class CategorySerializer(serializers.ModelSerializer):
    child_categories = RecursionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Categories
        fields = ['CategoryID', 'CategoryName', 'ParentCategoryID', 'child_categories']