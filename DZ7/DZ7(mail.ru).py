from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import unicodedata
from pymongo import MongoClient

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
time.sleep(3)

driver.get('https://m.mail.ru/inbox/')
WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((
                By.CLASS_NAME,'msglist'
            ))
        )
#letter_link = driver.find_element_by_xpath("//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']/@href")
letter_link = driver.find_element(By.CSS_SELECTOR, 'table.msglist a.messageline__link').get_attribute('href')
# print(letter_link)
# name = driver.find_element_by_class_name('messageline__from').text
# print(name)
def parse_mail(start_page:str):
    driver.get(start_page)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((
            By.CLASS_NAME, 'footer'
        )))
    data = {
        'url': driver.current_url,
        'header': driver.find_element(By.CSS_SELECTOR,'span.readmsg__theme').text.replace('\n','').replace('\t',''),
        'sender':driver.find_element(By.CSS_SELECTOR, 'span.readmsg__addressed-word ~ a').text,
        'date': driver.find_element(By.CSS_SELECTOR,'span.readmsg__mail-date').text,
        'text': unicodedata.normalize('NFKD', driver.find_element(By.ID,'readmsg__body').text).replace('\n','').replace('\t','').replace('  ','')
    }
    next_link = driver.find_elements(By.CSS_SELECTOR, 'div.readmsg__horizontal-block__right-block a.readmsg__text-link')
    if (next_link):
        return data,next_link[0].get_attribute('href')
    else:
        return data, None

# print(parse_mail(letter_link))
class Parser:
    def __init__(self,start_page: str):
        self.next = start_page
        self.data = None
        self.total = 0
    def __iter__(self):
        return self

    def __next__(self):
        if self.next:
            self.total += 1
            self.data,self.next = parse_mail(self.next)
            return self.data
        else:
            raise StopIteration

client = MongoClient('localhost', 27017)
db = client.selenium
collection = db['email']

parser = Parser(letter_link)
for letter in parser:
    print(letter['header'])
    if collection.update_one({'_id':letter['url']},{'$set':letter},upsert=True).matched_count != 0:
        break
print (parser.total)

driver.quit()

# mails = driver.find_element_by_class_name('js-tooltip-direction_letter-bottom')
# driver.get(mails.get_attribute('href'))
##time.sleep(1)
#print(driver.find_elements_by_class_name('thread__subject thread__subject_pony-mode'))
#print(driver.find_element_by_id('ph_mail'))
#print(driver.find_elements_by_class_name('letter__date').text)
##print(driver.find_elements_by_xpath("//div[@class='letter__date']//text()"))
#print(driver.find_element_by_class_name('letter__contact-item').text)
#print(autor)