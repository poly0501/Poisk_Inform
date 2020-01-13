from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
main_link="https://hh.ru"
vacancy_n = "Python"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"}
page="0"
html = requests.get(main_link+ "/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=" + vacancy_n + "&page="+page,headers=headers).text
parsed_html = bs(html,"lxml")
#next_main = parsed_html.find("div",{"data-qa":"pager-block"})
vacancy_block = parsed_html.find("div",{"class":"vacancy-serp"})
vacancy_list = vacancy_block.findAll("div",{"data-qa":"vacancy-serp__vacancy"})
next = parsed_html.find("a", {"class": "HH-Pager-Controls-Next"})["href"]
print(next)

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


def red_val(val,Smax,Smin):
    if val == "USD":
        val = "RUB"
        print(Smax)
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
        print(Smax)
        Smax = Smax * 69.47
        Smin = Smin * 69.47
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



def inf():
    vacancy_data = {}
    main_info = vacancy.find("a", {"class": "bloko-link HH-LinkModifier"})
    vacancy_name = main_info.getText()
    vacancy_link = main_info["href"]
    address = vacancy.findAll("div", {"class": "vacancy-serp-item__meta-info"})[1].getText()
    salary = vacancy.find("div",{"class": "vacancy-serp-item__sidebar"}).getText().replace("-", " - ")
    currency = parse_currency(salary)
    salary = parse_salary(salary)
    money = red_val(currency, salary[1], salary[0])

    vacancy_data["name"] = vacancy_name
    vacancy_data["link"] = vacancy_link
    vacancy_data["salary_min"] = money[2]
    vacancy_data["salary_max"] = money[1]
    vacancy_data["currency"] = money[0]
    vacancy_data["address"] = address
    vacancys.append(vacancy_data)

#Выводим две страницы подряд 
vacancys = []
for i in range(2):
    if next != "":
        for vacancy in vacancy_list:
            inf()
        html = requests.get(main_link + next,headers=headers).text
        parsed_html = bs(html, "lxml")
        vacancy_block = parsed_html.find("div", {"class": "vacancy-serp"})
        vacancy_list = vacancy_block.findAll("div", {"data-qa": "vacancy-serp__vacancy"})
        next = parsed_html.find("a", {"class": "HH-Pager-Controls-Next"})["href"]
    else:
        for vacancy in vacancy_list:
            inf()
pprint(vacancys)




