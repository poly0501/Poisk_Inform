from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import time
import json

chrome_options=Options()
chrome_options.add_argument('start-maximized')
#chrome_options.add_argument('--headless')


driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')
print('Открыта главная страница')
pages = 0

#не сработало
# while True:
#     try:
#         more_btn = WebDriverWait(driver,10).until(
#             EC.presence_of_all_elements_located((
#                 By.CLASS_NAME,'next-btn sel-hits-button-next'
#             ))
#         )
#         #more_btn = driver.find_element_by_class_name('special-offers__more-btn')
#         more_btn.click()
#         pages+=1
#         print(f'Обработаны {pages} продуктов')
#     except Exception as e:
#         print(e)
#         break

block = driver.find_elements_by_css_selector('div.sel-hits-block')[0]
last_btn = block.find_elements_by_css_selector('div.carousel-paging > a')[-1]
driver.execute_script("arguments[0].click();", last_btn)

goods = block.find_elements_by_css_selector('ul.accessories-product-list > li div.c-product-tile-picture__holder > a[data-product-info]')
json_raw = [e.get_attribute('data-product-info') for e in goods]
json_parser = [json.loads(e) for e in json_raw]
urls = [e.get_attribute('href') for e in goods]
total = list(zip(urls, json_parser))

client = MongoClient('localhost', 27017)
db = client.selenium
collection = db['mvideo']
for product in total:
    collection.update_one({'_id': product[0]}.{'$set': product[1]},upsert=True)

