from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
from pymongo import MongoClient
from pprint import pprint


chrome_options=Options()
chrome_options.add_argument('start-maximized')
#chrome_options.add_argument('--headless')

driver = webdriver.Chrome()
driver.get('https://account.mail.ru/login')
time.sleep(2)

elem = driver.find_element_by_name('Login')
elem.send_keys('study.ai_172')
elem.send_keys(Keys.RETURN)
time.sleep(1)

elem = driver.find_element_by_name('Password')
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)
time.sleep(5)

first_letters = driver.find_element_by_xpath("//div[@class='dataset__items']/a[1]")
print(first_letters)
datas = []
# for f in first_letters:

driver.get(first_letters.get_attribute('href'))
time.sleep(3)

next_s = driver.find_element_by_xpath("//div[@class='portal-menu-element portal-menu-element_next portal-menu-element_expanded portal-menu-element_not-touch portal-menu-element_pony-mode']")

while (next_s)!='':
    data = {}
    url = driver.current_url
    header = driver.find_element_by_class_name('thread__subject-line').text
    autor = driver.find_element_by_xpath("//div[@class='letter__author']/span[@class='letter__contact-item']").text
    # text = unicodedata.normalize('NFKD', driver.find_element_by_id('templateBody_mailru_css_attribute_postfix').text) #Читает только текстовые сообщения(На фотографиях вылетает)
    text = unicodedata.normalize('NFKD', driver.find_element_by_xpath("//div[@class='letter-body__body-content']").text)
    date = driver.find_element_by_xpath("//div[@class='letter__author']/div[@class='letter__date']").text

    data["url"] = url
    data["header"] = header
    data["autor"] = autor
    data["text"] = text
    data["date"] = date
    datas.append(data)
    #print(datas)

    next_s = driver.find_element_by_xpath("//div[@class='portal-menu-element portal-menu-element_next portal-menu-element_expanded portal-menu-element_not-touch portal-menu-element_pony-mode']")
    next_s.click()
    time.sleep(3)




client = MongoClient('localhost', 27017)
db = client.selenium
collection = db['email']

# collection.insert_many(datas)
# object = collection.find()
# for obj in object:
#     pprint(obj)


def do_insert():
    for d in datas:
        collection.update_one({"_id": d["_id"]},
                         {"$set": d},
                         upsert=True)

# Загрузка и
# Добавление новых писем 
do_insert()


