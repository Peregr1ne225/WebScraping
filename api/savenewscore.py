import os
import django

import sys
sys.path.insert(0, "C:\\Users\\champ\\Downloads\\499\\my_project\\WebScapping")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebScapping.settings')
django.setup()

from thefuzz import fuzz
from api.models import Products
from django.db.models import Max

def check_update(product_id, new_name):
    old_data = Products.objects.get(ProductID=product_id)
    old_name = old_data.ProductName
    product_db = Products.objects.all()

    if old_name == new_name and old_data.SimilarScore == 100:
        print("Product name is the same as the old one, and the similarity score is 100")
        return None, None
    for product in product_db:
        if product.ProductID == product_id:
            continue
        score = fuzz.ratio(product.ProductName, new_name)
        if score == 100:
            return product.SimilarGroup, 100
    if old_data.SimilarScore == 100:
        return old_data.SimilarGroup, 100
    else:
        max_group = get_max_group()
        return max_group + 1, 100
        
def get_max_group():
    max_similar_group_value = Products.objects.aggregate(max_similar_group=Max('SimilarGroup'))['max_similar_group']
    if max_similar_group_value is None:
        max_similar_group_value = 0
    return max_similar_group_value

if __name__ == "__main__":
    print("This is function module")
else:
    pass