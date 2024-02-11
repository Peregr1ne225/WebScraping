import SeleniumScrap
import time
from save_to_DB import save_list

error_list = []
loop_time = []

def get_menu():
    list_link = []
    soup = SeleniumScrap.connect('https://www.advice.co.th')
    
    for menu in soup.find_all("li", {"class":"menu-m-product-main"}):
        for item in menu.find_all("li", {"class":"menu-link"}):
            if item.find("a") is not None:
                list_link.append(item.find("a").get("href"))
    
    return list_link

def get_sub():
    list_link = get_menu()
    print(list_link)
    print(len(list_link))
    start_op = time.time()
    
    for link in list_link:
        print("Begin:", link)
        start_loop = time.time()
        #link = "https://www.advice.co.th//productcorporate/กล้อง-ip-camera"
        soup = SeleniumScrap.connect(link)
        #soup = SeleniumScrap.connect("https://www.advice.co.th//productcorporate/monitor")
        if soup.find(id="filter-cate") is not None:
            if soup.find(id="filter-cate").find_all("div", {"class":"custom-control"}) == []:
                continue
            last_menu = soup.find(id="filter-cate").find_all("div", {"class":"custom-control"})[-1].get_text().strip()
        else:
            continue
        
        xpath_last = "//div[@item-dtlcategory=\"" + last_menu + "\"]"
        soup_item, bool_load = SeleniumScrap.wait_to_load_last(xpath_last, 10)
        print(bool_load)
        if bool_load is False:
            error_list.append("LastItem:"+link)
        list_menu = get_item(soup_item, last_menu)
        save_list(list_menu)
        end_loop = time.time()
        loop_time.append(end_loop-start_loop)
        print("Operation in loop was completed Estimation time was", end_loop- start_loop, "Seconds\n")
    end_op = time.time()
    print("Operation was ompleted Estimation time was", end_op-start_op)
    
    with open('Advice.txt','w') as f:
        f.write(str(end_op-start_op))
        f.write("\n")
        for t in loop_time:
            f.write(str(t) + "\n")
    if len(error_list) > 0:
        with open('AdviceError.txt','w') as f:
            for error in error_list:
                f.write(error+"\n")
    
    SeleniumScrap.quit()

def get_item(soup, last):
    list_menu = []
    head_cate = soup.find_all("li", {"class":"breadcrumb-item"})[1].text
    #print(head_cate)
    for menu in soup.find_all("div", {"class":"item"}):
        product_code = menu.get("code-product-item")
        product_name = menu.get("item-name")
        url = "No Link"
        
        for a in menu.find_all("a"):
            if a.get("href") is not None:
                url = a.get("href")
                break
            
        brand = menu.get("item-brand")
        price = menu.find("div", {"class":"online-btn-cart"}).get("data-price")
        img = menu.find("img", {"class":"img-fluid"}).get("src")
        desc = menu.find("div", {"class":"item-spec"}).text
        if menu.get("item-category") == "":
            path_to_file = head_cate + "//" + menu.get("item-subcategory") + "//" + menu.get("item-dtlcategory")
        else:
            path_to_file = menu.get("item-category") + "//" + menu.get("item-subcategory") + "//" + menu.get("item-dtlcategory")
        stock = menu.find("div", {"class":"online-btn-cart"}).get("stock")
        list_item = [product_code, product_name, url, brand, price, stock, img, desc, path_to_file]
        if menu == soup.find_all("div", {"class":"item"})[-1]:
            print("Last Item:",list_item)
            if menu.get("item-dtlcategory") != last:
                print("Fuck You Advice")
                error_list.append("NotLast:"+last)
        list_menu.append(list_item)
    print(list_menu[-1])
    list_menu.sort()

    return list_menu

if __name__ == '__main__':
    get_sub()