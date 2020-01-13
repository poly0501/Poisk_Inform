import requests
from lxml import html
from pprint import pprint
main_link="https://lenta.ru"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"}
response = requests.get(main_link+"/rubrics/science/").text
root = html.fromstring(response)


def chist(a):
    a = str(a).replace("[", "").replace("]", "").replace("'", "").replace("\\xa0"," ")
    return a


#Если нам даётся только часть ссылки, мы её дополняем
def ss(links):
    links = chist(links)
    if str(links)[0] == "/":
        links = (main_link + links)
    return links


def date_time(date_1,date_2):
    date = str(date_1) + " в " + str(date_2)
    date = chist(date)
    return (date)


def inf():
    news_data = {}
    date_1 = news_bl.xpath(".//div[1]/span[1]/text()")
    date_2 = news_bl.xpath(".//div[1]/span[1]/span[1]/text()")
    date = date_time(date_1,date_2)
    link = news_bl.xpath(".//div[2]/h3[1]/a[1]/@href")
    link = ss(link)
    name = news_bl.xpath(".//div[2]/h3[1]/a[1]/span/text()")
    name = chist(name)
    news_data["name"] = name
    news_data["link"] = link
    news_data["date"] = date
    news_1.append(news_data)


news_1 = []
news_block = root.xpath("//div[@class='row js-content']/div/section[1]/div[@class='item news b-tabloid__topic_news']")
for news_bl in news_block:
    inf()
#pprint(news_1)

from pymongo import MongoClient
from pprint import pprint

client = MongoClient("localhost",27017)
db = client["db_news3"]
News = db.News

News.insert_many(news_1)
object = News.find()
for obj in object:
    pprint(obj)


def do_insert():
    for news in news_1:
        News.update_one({"_id": news["_id"]},
                         {"$set": news},
                         upsert=True)


#Добавление новых новостей
do_insert()

