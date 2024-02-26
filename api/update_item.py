import os
import django
import sys
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time

sys.path.insert(0, "C:\\Users\\champ\\Downloads\\499\\my_project\\WebScapping")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebScapping.settings')
django.setup()
#from SeleniumScrap import connect
from api.models import *

def update(id):
    try:
        product = Products.objects.get(ProductID=id)
    except Products.DoesNotExist:
        print("No Product")
        return "No Product"
    list_item = []
    list_item.append(product.ProductID)
    url = product.URL
    print(product.RetailID.Retail)

    if product.RetailID.Retail == "Banana Online":
        item = bananaItem(url)
    elif product.RetailID.Retail == "JIB":
        item = jibItem(url)
    elif product.RetailID.Retail == "Advice":
        item = adviceItem(url)
    
    if item is None:
        delete_product = Products.objects.get(ProductID=list_item[0])
        delete_product.delete()
        print("No Element")
        return "No Element"
    else:
        list_item = list_item + item
        add_newdata(list_item)
        print(list_item)
        return "Update Complete"

def bananaItem(url):
    list_item = []
    soup = connect(url)
    print(soup.find("div", {"class":"page-not-found"}))
    if soup.find("div", {"class":"page-not-found"}) is not None:
        print("No Element")
        return None
    
    #Price
    try:
        price = soup.find_all("div", {"class":"product-detail-summary"})[1]
        price = price.find("div", {"class":"selling-price"}).text.strip().replace(",", "").replace("฿", "")
        
        price = float(price)
    except ValueError:
        price = 0
    list_item.append(price)
    
    #Stock
    if (soup.find("div", {"class":"product-quantity"})) is not None:
        if soup.find("div", {"class":"product-quantity"}).find("div", {"class":"warning-msg"}):
            stock = "Out of Stock"
        else:
            stock = "In Stock"
    else:
        print("No Element")
        return None
    list_item.append(stock)

    return list_item

def jibItem(url):
    list_item = []
    soup = connect(url)
    
    if soup.find("div", {"id":"price_box"}) is None:
        print("No Element")
        return None
    
    #Price
    price = soup.find("div", {"class":"price_block"}).find("strong").text.strip().replace(",", "")
    try:
        price = float(price)
    except ValueError:
        price = 0
    list_item.append(price)

    #Stock
    if soup.find("button", {"class":"out_stock"}):
        stock = "Out of Stock"
    elif soup.find("div", {"class":"cart_modal"}):
        stock = "In Stock"
    list_item.append(stock)

    return list_item

def adviceItem(url):
    list_item = []
    soup = connect(url)

    if soup.find("div", {"class":"product-views"}) is None:
        print("No Element")
        return None

    #Price
    try:
        price = soup.find("span", {"class":"sale"}).text.strip().replace(",", "").replace(".-", "")
        price = float(price)
    except:
        price = 0
    list_item.append(price)
    
    #Stock
    if soup.find("div", {"class":"btn-addcart"}) is not None:
        stock = "In Stock"
    else:
        stock = "Out of Stock"
    list_item.append(stock)
    
    return list_item

def connect(url):
    options = Options()
    #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")
    options.use_chromium = True
    driver = webdriver.Edge(options=options)
    # driver.set_window_position(2000, 0)
    # driver.maximize_window()
    driver.get(url)
    time.sleep(3)
    return BeautifulSoup(driver.page_source, 'html.parser')

def add_newdata(list_item):
    product = Products.objects.get(ProductID=list_item[0])
    old_price = "{:.2f}".format(float(product.Price))
    new_price = "{:.2f}".format(float(list_item[1]))
    #Update Price
    if old_price != new_price:
        product.Price = new_price
        product.save()
        create_log(product, "Price", old_price, product.Price)
    
    #Update Stock
    old_stock = product.Stock
    if old_stock != list_item[2]:
        product.Stock = list_item[2]
        product.save()
        create_log(product, "Stock", old_stock, list_item[2])

def create_log(id, attrib, old, new):
    new_log = Logs.objects.create(
        ProductID = id,
        EditBy = "System",
        EditAttrib = attrib,
        OldData = old,
        NewData = new,
    )
    print(new_log)
    
if __name__ == "__main__":
    print("This is functoon module")
    #update("A0157531")
else:
    pass