#Соберём спортивные новости с сойта mail.ru

import requests
from lxml import html
from pprint import pprint
main_link="https://sportmail.ru/"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"}
response = requests.get(main_link).text
root = html.fromstring(response)


def inf():
    news_data = {}
    name = news_bl.xpath(".//div/div/a[@class='hdr__text']/span/text()")
    links = news_bl.xpath(".//div/div/a[@class='hdr__text']/@href")
    istochnik = news_bl.xpath(".//div[2]/div[@class='newsitem__params']/span[@class='newsitem__param']/text()")
    date = news_bl.xpath(".//div[2]/div[@class='newsitem__params']/span[@class='newsitem__param js-ago']/@datetime")
    news_3 = []
    news_3_data = {}
    news_gl_link = news_bl.xpath(".//span[2]/a/@href")
    news_gl_name = news_bl.xpath(".//span[2]/a/span/text()")
    news_3_data["name"] = news_gl_name
    news_3_data["link"] = news_gl_link
    news_3.append(news_3_data)
    news = news_bl.xpath(".//ul[1]/li")
    news_2 = []
    for n in news:
        news_2_data = {}
        link__ = n.xpath(".//span[1]/a[1]/@href")
        name__ = n.xpath(".//span[1]/a[1]/span[1]/text()")
        news_2_data["name"] = name__
        news_2_data["link"] = link__
        news_2.append(news_2_data)

    news_data["name_categor"] = name
    news_data["date"] = date
    news_data["istochnik"] = istochnik
    news_data["news"] = news_2
    news_data["news_glav"] = news_3
    news_1.append(news_data)


news_1 = []
news_block = root.xpath("//div[@class='wrapper js-module']/div[@class='cols cols_margin cols_percent']/div[@class='cols__wrapper']/div")
for news_bl in news_block:
    inf()
#pprint(news_1)

from pymongo import MongoClient
from pprint import pprint

client = MongoClient("localhost",27017)
db = client["db_news1"]
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
