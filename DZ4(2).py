import requests
from lxml import html
from pprint import pprint
main_link="https://yandex.ru/news"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"}
response = requests.get(main_link).text
root = html.fromstring(response)


#разделяем на две части: istochnik и time
def t_i(data_string):
    data_string = str(data_string).replace("'","").replace("\\xa0"," ").replace("[","").replace("]","")
    n = len(data_string)
    data_list = data_string.split()
    if len(data_list)==2:
        time = str(data_list[1])
        ist = str(data_list[0])
    elif len(data_list)==3:
        if data_list[1] == "вчера":
            time = str(data_list[2])
            ist = str(data_list[0])
        else:
            time = str(data_list[2])
            ist = str(data_list[0])+" "+str(data_list[1])
    elif len(data_list)==4:
        if data_list[2] == "вчера":
            time = str(data_list[2]) + str(data_list[3])
            ist = str(data_list[0])+" "+str(data_list[1])
        else:
            time = str(data_list[3])
            ist = str(data_list[0])+" "+str(data_list[1])+str(data_list[2])
    elif len(data_list) == 5:
        if data_list[3] == "вчера":
            time = str(data_list[3]) + str(data_list[4])
            ist = str(data_list[0]) + str(data_list[1]) + str(data_list[2])
        else:
            time = str(data_list[1])
            ist = str(data_list[0])
    return ist, time

#Если нам даётся только часть ссылки, мы её дополняем
def ss(link):
    link = str(link).replace("[", "").replace("]", "").replace("'", "")
    if str(link)[0] == "/":
        link = (main_link + link)
    return link

def inf():
    news_data = {}
    name = news_bl.xpath(".//div[1]/a[1]/text()")
    table = news_bl.xpath(".//div[1]/table[1]/tr/td")
    news_2 = []
    for t in table:
        news_2_data = {}
        name__ = t.xpath(".//div[1]/div[1]/h2[1]/a/text()")
        link = t.xpath(".//div[1]/div[1]/h2[1]/a/@href")
        link = ss(link)
        ist_and_time = t.xpath(".//div[1]/div[2]/div/text()")
        ist_and_time = t_i(ist_and_time)
        news_2_data["name"] = name__
        news_2_data["link"] = link
        news_2_data["istochnik"] = ist_and_time[0]
        news_2_data["time"] = ist_and_time[1]
        news_2.append(news_2_data)

    news_data["name_categor"] = name
    news_data["news"] = news_2
    news_1.append(news_data)


news_1 = []
news_block = root.xpath("//div[@class='page-content']/div[@class='page-content__cell']/div[@class='page-content__fixed page-content__fixed_middle']")
for news_bl in news_block:
    inf()
#pprint(news_1)

from pymongo import MongoClient
from pprint import pprint

client = MongoClient("localhost",27017)
db = client["db_news2"]
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