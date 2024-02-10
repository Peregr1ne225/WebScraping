import SeleniumScrap
import time
from save_to_DB import save_list
import math

error_list = []
loop_time = []

def get_menu():
    list_link = []
    soup = SeleniumScrap.connect('https://www.jib.co.th/web/')
    
    for menu in soup.find("div", {"class":"menu_back"}).find_all("dd"):
        list_link.append(menu.find("a").get("href"))
    
    return list_link

def get_sub():
    list_link = get_menu()
    print(list_link)
    start_op = time.time()

    for link in list_link:
        print("Begin:", link)
        #link = "https://www.jib.co.th/web/product/product_list/3/670"
        start_loop = time.time()
        cate_soup = SeleniumScrap.connect(link)
        cate_soup, path = get_path(cate_soup, link)
        #print(path)
        get_brand_cate(cate_soup, link, path)
        end_loop = time.time()
        
        print("Operation in loop was completed Estimation time was", end_loop- start_loop, "Seconds\n")
        loop_time.append(end_loop-start_loop)
    end_op = time.time()
    print("Operation was ompleted Estimation time was", end_op-start_op, error_list)
    
    with open('JIB.txt','w') as f:
        f.write(str(end_op-start_op))
        f.write("\n")
        for t in loop_time:
            f.write(str(t) + "\n")
    if len(error_list) > 0:
        with open('BananaError.txt','w') as f:
            for error in error_list:
                f.write(error+"\n")

    SeleniumScrap.quit()

def get_path(soup, link): #Path of Category
    path = []

    try:
        for i in soup.find("div", {"class":"searchleft"}).find_all("a"): #find_path
            path.append(i.text)
    except:
        SeleniumScrap.quit()
        time.sleep(10)
        soup = SeleniumScrap.connect(link)
        for i in soup.find("div", {"class":"searchleft"}).find_all("a"): #find_path
            path.append(i.text)
    
    path_str = '//'.join(path[1::])
    
    return soup, path_str

def get_brand_cate(soup, link, path):
    brand_cate = soup.find_all("div", {"class":"brand_ch"})
    
    if len(brand_cate) == 0:
        return
    elif len(brand_cate) == 1:
        get_brand(link, path, brand_cate[0], link)
    else:
        for brand in brand_cate:
            link_brand = link + "/0?brand=" + brand.find("input").get("value")
            SeleniumScrap.connect(link_brand)
            get_brand(link_brand, path, brand, link_brand)

def get_brand(link, path, brand, link_brand):
    item_brand = brand.text.strip() #brand
    print(brand.find("input").get("value"))
    stock = SeleniumScrap.wait_to_click(link_brand, "sh_stock", 0)
    
    if stock is None:
        soup_item = SeleniumScrap.get_soup()
        error_list.append("Stock:"+link)
    else:
        soup_item = SeleniumScrap.check_box_run(stock)
        if soup_item is None:
            error_list.append("ClickFail:"+link)
            return
    
    page = int(soup_item.find("div", {"class":"panel-body"}).find("span").text)
    page = math.ceil(page/100)
    if page > 2:
        get_item(soup_item, path, item_brand) #first page
        for i in range(1, page): #next page
            SeleniumScrap.connect(link+"/"+str(i*100)+"?brand=" + brand.find("input").get("value"))
            get_item(soup_item, path, item_brand)
    elif page == 0:
        print("No Item go next loop")
        return
    else:
        get_item(soup_item, path, item_brand)

def get_item(soup, path, brand):
    list_menu = []
    for item in soup.find_all("div", {"class":"reladiv"}): #item
        product_code = "j" + item.find("div", {"class":"buy_promo"}).get("data-id") #code
        product_name = item.find("span", {"class":"promo_name"}).text #name
        url = item.find("div", {"class":"size_img"}).find("a").get("href")
        
        try:
            price = float(item.find("p", {"class":"price_total"}).text.strip().replace(".-", "").replace(",", "")) #price
        except ValueError:
            price = 0
        
        stock = item.find("div", {"class":"buy_promo"}).text #stock
        img = "https://www.jib.co.th"+item.find("img", {"class":"imgpspecial"}).get("src") #img
        desc = item.find("div", {"class":"description"}).text.replace("\n", "") #desc
        list_item = [product_code, product_name, url, brand, price, stock, img, desc, path]
        list_menu.append(list_item)
    list_menu.sort()
    print(list_menu[-1])
    save_list(list_menu)
     
if __name__ == '__main__':
    get_sub()