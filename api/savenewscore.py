from thefuzz import fuzz
from .models import Products
from django.db.models import Max

def check_update(product_id, new_name):
    old_name = Products.objects.get(ProductID=product_id).ProductName
    product_db = Products.objects.all()

    if old_name == new_name:
        print("Product name is the same as the old one")
        return None
    for product in product_db:
        score = fuzz.ratio(product.ProductName, new_name)
        if score == 100:
            return product.SimilarGroup
        else:
            max_group = get_max_group()
            return max_group + 1
        
def get_max_group():
    max_similar_group_value = Products.objects.aggregate(max_similar_group=Max('SimilarGroup'))['max_similar_group']
    if max_similar_group_value is None:
        max_similar_group_value = 0
    return max_similar_group_value

if __name__ == "__main__":
    print("This is function module")
else:
    pass