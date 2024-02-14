from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('ProductID', 'ProductName', 'BrandID', 'Price', 'Stock', 
                  'Description', 'URL', 'PicURL', 'CategoryID', 'RetailID',
                  'DateEdit', 'SimilarGroup', 'DateCreate')