#import django_connect
import os
import django
import sys

sys.path.insert(0, "C:\\Users\\champ\\Downloads\\499\\my_project\\WebScapping")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebScapping.settings')
django.setup()

import re #regular expression

from api.models import *
from django.db.models import Max
from thefuzz import fuzz
from django.core.exceptions import ObjectDoesNotExist

#Check Product in DB
def save_list(list_item):
    for product in list_item:
        if Products.objects.filter(URL=product[2]).exists(): #Check if URL already exist same url suposerd to be same product
            print(f"{product[2]} Already Exist")
            check_update(product) #Check for update important data
        else:
            create_new_db(product) #Create new product

#Create New Product
def create_new_db(product):
    if "b" in product[0]: #Check if Banana to create new ID
        last_product = Products.objects.filter(RetailID=3).order_by('ProductID').last()
        if last_product is None:
            p_id = "B000001" #First Product
        else: 
            p_id = "B" + (str(int(last_product.ProductID[1:]) + 1).zfill(6)) #New Product with B+6DIGIT
    else: #Another Retailer
        p_id = product[0]
    
    brand = save_brand(product[3])
    retail = save_retail(product[2])
    category = save_category(product[8])
    
    if Products.objects.filter(ProductID=p_id).exists(): #Check if ProductID already exist same id may have 2 url
        return
    #Create New Product
    new_product = Products.objects.create(
        ProductID = p_id,
        ProductName = product[1],
        BrandID = brand,
        Price = product[4],
        Stock = product[5],
        Description = product[7],
        URL = product[2],
        PicURL = product[6],
        CategoryID = category,
        RetailID = retail,
    )
    string_matching(new_product) #Check for similar product
    print(new_product) 
    
#Save Brand    
def save_brand(brand):
    brand = brand.upper()
    exist_brand, _ = Brands.objects.get_or_create(BrandName=brand) #Check if Brand already exist
    
    if _: #Insert New Brand
        print(f"Brand {brand} Created Successful")
    
    return exist_brand

#Save Retailer
def save_retail(retail_link):
    if "https://www.bnn.in.th/th/" in retail_link:
        return Retailers.objects.get(Retail="Banana Online")
    elif "www.advice.co.th" in retail_link:
        return Retailers.objects.get(Retail="Advice")
    else:
        return Retailers.objects.get(Retail="JIB")

#Save Category
def save_category(path):
    path_list = path_split(path) #Split Path
    parent_id = None #First Parent
    
    for cate in path_list: #Create Nested Category
        category, _ = Categories.objects.get_or_create(CategoryName=cate, ParentCategoryID=parent_id)
        parent_id = category #Set Parent for next category
    
    return category

#Split Path
def path_split(path):
    path = path.upper() #Upper Case
    path = path.replace("(", " ").replace(")", " ") #Replace ( and ) to space
    path_list = path.split("//") #Split by //
    path_list = [i.strip() for i in path_list] #Strip Space
    
    return path_list

#Check for Update
def check_update(product):
    try:
        old_product = Products.objects.get(URL = product[2])
    except Products.DoesNotExist:
        print("DuplicateURL same_product")
        return
    
    #Update Price
    old_price = "{:.2f}".format(float(old_product.Price))
    new_price = "{:.2f}".format(float(product[4]))
    if old_price != new_price:
        Products.objects.filter(URL = product[2]).update(Price = product[4])
        update_product = Products.objects.get(URL = product[2])
        create_log(update_product, "Price", old_product.Price, update_product.Price)
    
    #Update Stock
    if old_product.Stock != product[5]:
        Products.objects.filter(URL = product[2]).update(Stock = product[5])
        update_product = Products.objects.get(URL = product[2])
        print(f"Old Data: {old_product.Stock}, New Data: {update_product.Stock}")
    
    #Update PicURL when new picture come to product
    if old_product.PicURL != product[6]:
        Products.objects.filter(URL = product[2]).update(PicURL = product[6])
        update_product = Products.objects.get(URL = product[2])
        print(f"Old Data: {old_product.PicURL}, New Data: {update_product.PicURL}")
        create_log(update_product, "Pic", old_product.PicURL, update_product.PicURL)

#Create Log
def create_log(id, attrib, old, new):
    new_log = Logs.objects.create(
        ProductID = id,
        EditBy = "System",
        EditAttrib = attrib,
        OldData = old,
        NewData = new,
    )
    print(new_log)

# def DelItem():
#     Categories.objects.filter(CategoryID='7').delete()

# clean thai word
def data_clean(name):
    pattern = r"[\u0E00-\u0E7F]+"
    name = re.sub(pattern, "", name)
    name = name.replace("()", "")
    while True:
        if "  " in name:
            name = name.replace("  ", " ")
        else:
            break
    name.strip()
    print(name)
    return name

#Get Last Group
def get_max_group():
    max_similar_group_value = Products.objects.aggregate(max_similar_group=Max('SimilarGroup'))['max_similar_group']
    if max_similar_group_value is None:
        max_similar_group_value = 0
    return max_similar_group_value

#Check Similar Product
def string_matching(new_product):
    new_name = data_clean(new_product.ProductName).upper()
    max_similarity = 0
    retail = new_product.RetailID.RetailID
    # exlude the same retail beacuse same retail not suppose to be similar
    if retail == 1:
        products = Products.objects.exclude(RetailID=1)
    elif retail == 2:
        products = Products.objects.exclude(RetailID=2)
    else:
        products = Products.objects.exclude(RetailID=3)
    
    for product in products:
        product_name = data_clean(product.ProductName).upper() #Clean Thai Word and Upper Case
        similarity = fuzz.partial_token_sort_ratio(new_name, product_name) #Use Partial Token Sort Ratio
        if similarity > 90 and max_similarity < similarity: #If more than 90% and max similarity
            print(f"Similarity of {new_product.ProductID} and {product.ProductID} is {similarity}")
            max_similarity = similarity #Set Max Similarity
            new_product.SimilarGroup = product.SimilarGroup
            new_product.SimilarScore = similarity
            new_product.save()
            
    if new_product.SimilarGroup is None:
        max_similar = get_max_group()
        new_product.SimilarGroup = max_similar + 1
        new_product.SimilarScore = 100
        new_product.save()

if __name__ == '__main__':
    print("This is function module")
    #data_clean("VGA (การ์ดแสดงผล) ASUS GEFORCE GT 730 2GB DDR3 EVO (GT730-SL-2GD3-BRK-EVO)")
else:
    pass