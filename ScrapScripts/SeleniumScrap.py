from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

timeout = 30
sleep = 10

def start():
    global driver
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Edge(options = options)
    #driver = webdriver.Edge()
    driver.set_window_position(2000, 0)
    driver.maximize_window()

def connect(url):
    if "driver" not in globals(): #check first time run
        start() 
        if "www.jib.co.th" in url:
            driver.get("https://www.jib.co.th/web/lswitcher/switchlang/en")   
    try:
        driver.current_url #Check If Still Running
    except:
        start() #Not Run
        if "www.jib.co.th" in url:
            driver.get("https://www.jib.co.th/web/lswitcher/switchlang/en")   

    try:
        driver.get(url)
        if "www.jib.co.th" in url:
            element_present = EC.presence_of_element_located((By.ID, "jib_logo"))
            WebDriverWait(driver, 5).until(element_present)
    except:
        if "www.jib.co.th" in url:
            "Cloud Flare Running"
        driver.quit()
        time.sleep(1)
        connect(url)
    page = driver.page_source
    return BeautifulSoup(page, 'html.parser')

def wait_to_load_last(path, timeout):
    i = 0
    while True:
        try:
            print("Try")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            element_present = EC.presence_of_element_located((By.XPATH, path))
            WebDriverWait(driver, 5).until(element_present)
            cate_source = driver.page_source
            return BeautifulSoup(cate_source, 'html.parser'), True
        except:
            i = i+1
            if i > 10:
                timeout = timeout-1
                if timeout <= 0:
                    return BeautifulSoup(driver.page_source, 'html.parser'), False
                else:
                    driver.refresh()
                    i=0
            else:
                pass

def quit():
    driver.quit()

def wait_to_click(link, id, i):
    try:
        element_present = EC.element_to_be_clickable((By.ID, id))
        WebDriverWait(driver, timeout).until(element_present)
        stock = driver.find_element(By.ID, id) #checkbox
        
        return stock
    
    except TimeoutException:
        i = i+1
        if i > 5: #try 5 times
            stock = driver.find_element(By.ID, id)
            return None
        elif "www.bnn.in.th" in link:
            print("No Element")
            return None
        print("Timed out waiting for page to load")
        
        quit()
        time.sleep(sleep)
        connect(link)
        
        wait_to_click(link, id, i)

def check_box_run(stock):
    js_code = "arguments[0].scrollIntoViewIfNeeded();"
    if stock.is_selected(): #checked box
        time.sleep(3)
        driver.execute_script(js_code, stock)
        try:
            stock.click()
        except:
            print("Can not click")
            return None
    return BeautifulSoup(driver.page_source, 'html.parser')

def delete_run(stock):
    script = """
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """
    driver.execute_script(script, stock)

def click_expand_all(id):
    js_code = "arguments[0].scrollIntoViewIfNeeded();"
    while True:
        if len(driver.find_elements(By.CLASS_NAME, id)) == 2:
            break
        stock = driver.find_element(By.CLASS_NAME, id)
        driver.execute_script(js_code, stock)
        stock.click()
    return BeautifulSoup(driver.page_source, 'html.parser') 

def cloud_flare_skip(url):
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, "site-logo"))
        WebDriverWait(driver, timeout).until(element_present)
    except:
        driver.quit()
        time.sleep(sleep)
        start()
        driver.get(url)
        cloud_flare_skip(url)
    
    return BeautifulSoup(driver.page_source, 'html.parser')

def get_soup():
    return BeautifulSoup(driver.page_source, 'html.parser')

def presence_of_item(element):
    elements = EC.presence_of_all_elements_located((By.CSS_SELECTOR, element))
    WebDriverWait(driver, timeout).until(elements)
    return BeautifulSoup(driver.page_source, 'html.parser')

if __name__ == '__main__':
    print("This is function module")
else:
    pass