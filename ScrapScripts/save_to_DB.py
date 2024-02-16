import django_connect
import re
# from celery import Celery
# app = Celery('tasks', broker='amqp://guest:guest@localhost//')
from api.models import *

#@app.task
def save_list(list_item):
    for product in list_item:
        if Products.objects.filter(URL=product[2]).exists():
            print(f"{product[2]} Already Exist")
            check_update(product)
        else:
            create_new_db(product)

def create_new_db(product):
    print(product)
    brand = save_brand(product[3])
    retail = save_retail(product[2])
    category = save_category(product[8])
    new_product = Products.objects.create(
        ProductName = data_clean(product[1]),
        BrandID = brand,
        Price = product[4],
        Stock = product[5],
        Description = product[7],
        URL = product[2],
        PicURL = product[6],
        CategoryID = category,
        RetailID = retail,
    )
    print(new_product)
    
def save_brand(brand):
    brand = brand.upper()
    exist_brand, _ = Brands.objects.get_or_create(BrandName=brand)
    
    if _: #Insert New Brand
        print(f"Brand {brand} Created Successful")
    
    return exist_brand

def save_retail(retail_link):
    if "https://www.bnn.in.th/th/" in retail_link:
        return Retailers.objects.get(Retail="Banana Online")
    elif "www.advice.co.th" in retail_link:
        return Retailers.objects.get(Retail="Advice")
    else:
        return Retailers.objects.get(Retail="JIB")

def save_category(path):
    path_list = path_split(path)
    parent_id = None
    
    for cate in path_list:
        category, _ = Categories.objects.get_or_create(CategoryName=cate, ParentCategoryID=parent_id)
        parent_id = category
    if _:
        print(f"Catagory {cate} Created Successful")
    
    return category

def path_split(path):
    path = path.upper()
    path = path.replace("(", " ").replace(")", " ")
    path_list = path.split("//")
    path_list = [i.strip() for i in path_list]
    
    return path_list

def check_update(product):
    try:
        old_product = Products.objects.get(URL = product[2])
    except Products.DoesNotExist:
        print("DuplicateURL same_product")
        return
    old_price = "{:.2f}".format(float(old_product.Price))
    new_price = "{:.2f}".format(float(product[4]))
    if old_product.ProductName != product[1]:
        Products.objects.filter(URL = product[2]).update(ProductName = product[1])
        update_product = Products.objects.get(URL = product[2])
        create_log(update_product, "ProductName", old_product.ProductName, update_product.ProductName)
    
    if old_price != new_price:
        Products.objects.filter(URL = product[2]).update(Price = product[4])
        update_product = Products.objects.get(URL = product[2])
        create_log(update_product, "Price", old_product.Price, update_product.Price)

    if old_product.Stock != product[5]:
        Products.objects.filter(URL = product[2]).update(Stock = product[5])
        update_product = Products.objects.get(URL = product[2])
        print(f"Old Data: {old_product.Stock}, New Data: {update_product.Stock}")
        create_log(update_product, "Stock", old_product.Stock, update_product.Stock)
    
    if old_product.PicURL != product[6]:
        Products.objects.filter(URL = product[2]).update(PicURL = product[6])
        update_product = Products.objects.get(URL = product[2])
        print(f"Old Data: {old_product.PicURL}, New Data: {update_product.PicURL}")
        create_log(update_product, "Pic", old_product.PicURL, update_product.PicURL)

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
    pattern = r"[\u0E00-\u0E7F\s]"
    name = re.sub(pattern, "", name)
    name = name.replace("()", "")
    name.replace("  ", "")
    name.strip()
    return name

if __name__ == '__main__':
    print("This is function module")
    #check_update()
else:
    pass