import SeleniumScrap
import time
from save_to_DB import save_list

error_list = []
loop_time = []

def expand_cate():
    stock = SeleniumScrap.connect("https://www.bnn.in.th/en/p?in_stock=false&sort_by=relevance&page=1")
    stock = SeleniumScrap.wait_to_click("https://www.bnn.in.th/en/p?in_stock=false&sort_by=relevance&page=1", "ins-frameless-overlay", 0)
    
    if stock is not None:
        SeleniumScrap.delete_run(stock)
    soup_main = SeleniumScrap.click_expand_all("fa-plus")
    
    return soup_main

def get_menu(soup):
    list_name = []
    list_link = []
    
    for item in soup.find_all("a", {"class":"filter-category-item"}):
        list_link.append(item.get("href"))
        list_name.append(item.text)
    
    for i in range(len(list_name)):
        if "All" in list_name[i]:
            list_name[i] = ""
            list_name[i-1] = ""
            list_link[i] = ""
            list_link[i-1] = ""
        elif "Brand" in list_name[i] or "by-brand" in list_link[i]:
            list_name[i] = ""
            list_link[i] = ""
    
    while "" in list_name:
        list_name.remove("")
        list_link.remove("")
    
    print(list_link)
    return list_link

def get_path():
    soup = expand_cate()
    list_link = get_menu(soup)
    print(len(list_link))
    start_op = time.time()
    
    for sub_link in list_link:
        start_loop = time.time()
        
        link = "https://www.bnn.in.th" + sub_link
        SeleniumScrap.connect(link)
        soup = SeleniumScrap.cloud_flare_skip(link)
        
        if soup.find("h1", {"class":"page-title"}).text.strip() == "Page Not Found":
            error_list.append("NotFound:"+link)
            print("Page Not Found")
            continue
        
        if soup.find_all("li", {"class":"vmq-pagination-button"}) == []: #No Data
            error_list.append("NoItem:"+link)
            continue
        
        #find path
        path = []
        element = 'a.-text-bold'
        soup = SeleniumScrap.presence_of_item(element)
        for item_path in soup.find_all("a", {"class":"-text-bold"}):
            path.append(item_path.text.strip())
        if len(path) <= 1:
            print("error")
            error_list.append("PathError:"+link)
        path = "//".join(path)
        print(path)
        
        get_to_page(soup, path, link)

        end_loop = time.time()
        loop_time.append(end_loop-start_loop)
        print("Operation in loop was completed Estimation time was", end_loop-start_loop, "\n")
    
    end_op = time.time()
    print("Operation was ompleted Estimation time was", end_op-start_op, error_list)
    
    with open('Banana.txt','w') as f:
        f.write(str(end_op-start_op))
        f.write("\n")
        for t in loop_time:
            f.write(str(t) + "\n")
    
    if len(error_list) > 0:
        with open('BananaError.txt','w') as f:
            for error in error_list:
                f.write(error+"\n")
    
    SeleniumScrap.quit()

def get_to_page(soup, path, link): #All Page
    list_menu = []
    id = 0
    max_page = int(soup.find_all("li", {"class":"vmq-pagination-button"})[-1].text)
    print("This cate have:", max_page, "Page")
    
    for i in range(max_page):
        if i >= 1:
            url = link + "?page=" + str(i+1)
            SeleniumScrap.connect(url)
            soup = SeleniumScrap.cloud_flare_skip(url)
        menu, id = get_item(soup, path, id)
        list_menu = list_menu + menu
    
    print(list_menu[-1])
    save_list(list_menu)

def get_item(soup, path, id): #Per Page
    list_menu = []
    
    for item in soup.find_all("a", {"class":"product-link"}):
        id = id + 1
        name = item.find("div", {"class":"product-name"}).get("title")
        url = "https://www.bnn.in.th/" + "th" + item.get("href")[3::]
        brand = item.find("div", {"class":"product-label-brand"}).text.strip()
        price = item.find("div", {"class":"product-price"}).text.strip()
        price = price.replace("฿", "").replace(",", "").split("-")[0].strip()
        try:
            price = float(price)
        except:
            price = 0
        if item.find("div", {"class":"badge-inactive"}) is not None:
            stock = item.find("div", {"class":"badge-inactive"}).text.strip()
            if len(stock) > 25:
                stock = stock[0::24]
        else:
            stock = "Instock"
        pic = item.find("img", {"class":"image"}).get("src")
        if item.find("div", {"class":"product-short-attribute"}) is not None:
            desc = item.find("div", {"class":"product-short-attribute"}).text.strip()
        else:
            desc = ""
        
        list_item = ["b"+ str(id), name, url, brand, price, stock, pic, desc, path]
        list_menu.append(list_item)
    
    return list_menu, id

if __name__ == '__main__':
    get_path()