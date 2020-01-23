# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from pprint import pprint

class JobparserPipeline(object):

    def __init__(self):
        client = MongoClient('localhost',270717)
        self.mongo_base = client.vacansy_hh

    def process_item(self, item, spider):
        print("111111111111111111111111111")
        #print(item._values)
        name = ''
        links = ''
        address = ''
        min_price = 0
        max_price = 0
        currency = ''
        if spider.name == 'hhru':
            name = item._values["name"]
            print(name)
            links = item._values["links"]
            address = item._values["address"]
            print(address)
            salary = item._values["salary"].replace("-", " - ")
            currency = parse_currency(salary)
            print(currency)
            salary = parse_salary(salary)
            money = red_val(currency, salary[1], salary[0])
            max_price = money[1]
            min_price = money[2]
            print(min_price, max_price)
        elif spider.name=='superjob':
            name = item._values["name"]
            print(name)
            links = item._values["links"]
            address = item._values["address"]
            print(address)
            salary = item._values["salary"].replace("-", " - ")
            currency = parse_currency(salary)
            salary = parse_salary(salary)
            money = red_val(currency, salary[1], salary[0])
            max_price = money[1]
            min_price = money[2]
            print(min_price, max_price)
        rec = {"name": name,
               "links": links,
               "max_prise": max_price,
               "min_price": min_price,
               "max_price": max_price,
               "currency": currency,
               "address": address}
        self.new_record(rec)
        pprint(rec)
        collection = self.mongo_base[rec]
        collection.insert_one(item)
        return item


def parse_salary(data_string):
    if data_string == "":
        salary_min = 0
        salary_max = 0
    else:
        data_list = data_string.split()
        if data_list[0] == "от":
            salary_min = int(data_list[1] + data_list[2])
            salary_max = 0
        elif data_list[0] == "до":
            salary_max = int(data_list[1] + data_list[2])
            salary_min = 0
        elif len(data_list) == 6:
            salary_min = int(data_list[0] + data_list[1])
            salary_max = int(data_list[3] + data_list[4])
        else:
            salary_min = int(data_list[0] + data_list[1])
            salary_max = salary_min
    return salary_min, salary_max


def red_val(val,Smax,Smin):
    if Smax=="None":
        Smax = int(0)
    if Smin=="None":
        Smin = int(0)
    if val == "USD":
        val = "RUB"
        Smax = Smax * 61.91
        Smin = Smin * 61.91
    elif val == "бел.\xa0руб":
        val = "RUB"
        Smax = Smax * 29.35
        Smin = Smin * 29.35
    elif val == "KZT":
        val = "RUB"
        Smax = Smax *0.16
        Smin = Smin *0.16
    elif val == "EUR":
        val = "RUB"
        Smax = Smax * 69
        Smin = Smin * 69
    elif val == "грн.":
        val = "RUB"
        Smax = Smax * 2.61
        Smin = Smin * 2.61
    else:
        val = "RUB"
        Smax = Smax
        Smin = Smin
    if Smax==0:
        Smax=None
    if Smin==0:
        Smin=None
    return (val,Smax,Smin)


def parse_currency(data_string):
    if data_string == "":
        curr = None
    else:
        data_list = data_string.split()
        if len(data_list) == 3:
            curr = str(data_list[2])
        elif len(data_list) == 6:
            curr = str(data_list[5])
        elif len(data_list) == 4:
            curr = str(data_list[3])
        else:
            curr = None
    return curr