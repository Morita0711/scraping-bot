from selenium import webdriver
import re
import os
from datetime import date, datetime
from threading import Timer
from webdriver_manager.chrome import ChromeDriverManager
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)
def task(URL = "https://www.amazon.de/dp/B009YWLWWK"):
    filename = re.split("/", URL)[-1]
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
    chromeOptions.add_argument('user-agent=Mozilla/5.0 (Wind ows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    chromeOptions.add_argument("--log-level=3")
    driver = webdriver.Chrome(ChromeDriverManager().install(),service_log_path='NUL')
    driver.maximize_window()
    driver.get(URL)
    css_selector = 'input[id="add-to-cart-button"]'
    button_element = driver.find_element_by_css_selector(css_selector)
    button_element.click()
    driver.implicitly_wait(10)

    css_selector1 = 'form[id="attach-view-cart-button-form"] > span > span > input'
    try:
        driver.find_element_by_css_selector(css_selector1).click()
        driver.implicitly_wait(10)
    except Exception:     
        driver.find_element_by_css_selector('a[id="hlb-view-cart-announce"]').click()

    css_selector2 = 'span[id="a-autoid-0-announce"]'
    button_element2 = driver.find_element_by_css_selector(css_selector2)
    button_element2.click()
    driver.implicitly_wait(10)

    css_selector4 = 'li[aria-labelledby="quantity_10"] > a'
    button_element4 = driver.find_element_by_css_selector(css_selector4)
    button_element4.click()
    driver.implicitly_wait(10)

    css_selector5 = 'input.sc-update-quantity-input:nth-of-type(1)'    
    button_element5 = driver.find_element_by_css_selector(css_selector5)
    button_element5.send_keys(999)
    driver.implicitly_wait(10)

    css_selector6 = 'a[id="a-autoid-1-announce"]'
    button_element6 = driver.find_element_by_css_selector(css_selector6)
    button_element6.click()
    driver.implicitly_wait(10)

    driver.execute_script("window.history.go(-1)")

    button = driver.find_elements_by_xpath('//a[contains(@class, "a-touch-link")]')
    for my_href in button:
        driver.get(my_href.get_attribute("href"))
    driver.implicitly_wait(10)

    elem = driver.find_element_by_css_selector("#aod-filter-offer-count-string")
    num = int(re.sub('[^0-9]', "", elem.text))
    title = driver.find_element_by_css_selector("#titleSection").get_attribute("innerText")
    print(title)
    send_str = str(title) + os.linesep

    for i in range(num):
        stock_selector = '#aod-offer-qty-dropdown-component-'+ str(i+1) +' span[data-action="select-aod-qty-option"]:nth-last-of-type(1)'
        price_selector = '#aod-price-1 span.a-offscreen'
        stock = 0
        price = ""

        try:
            stock = re.sub('[^0-9]', "", driver.find_element_by_css_selector(stock_selector).get_attribute("innerText"))
        except:
            stock = 0
        price = driver.find_element_by_css_selector(price_selector).get_attribute("innerText")
        send_str += "   " + str(stock)
        send_str += "   " + price
        send_str += os.linesep
        try:
            with open(filename + ".txt", 'a') as highscore:
                highscore.write(send_str)
        except IOError:
            with open(filename + ".txt", 'w') as highscore:
                highscore.write(send_str)

address = input("Please input your URL:")
timeframe = input("Do you want the timeframe: A) Set Timeframe B) Don't want the Timeframe. [A/B]? : ")
time = 0
if timeframe == "A":
    time = input("Please Set Time:")
_x = datetime.today()


def set_time(time):
    
    x = datetime.today()
    task(address)
    y = x.replace(day=x.day+1, hour=int(time), minute=0, second=0, microsecond=0)
    delta_t = y - x
    secs = delta_t.seconds + 1
    t = Timer(secs, task(address))
    t.start()
    
if timeframe == "A":
    set_time(time)
elif timeframe == "B":
    task(address)
