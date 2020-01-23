# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.xpath("div[@class='_3syPg _3P0J7 _9_FPy']/@href").extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//div[@class='_3mfro CuJz5 PlM3e _2JVkc _3LJqf']/text()").extract()
        salary = response.xpath("//span[@class='_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz']/text()").extract_first()
        links = response.xpath("//div[@class='icMQ_ _1QIBo f-test-link-Programmist_Python_(Python\Django\HTML\CSS\JS) _2JivQ _3dPok']/@href").extract_first()
        address=response.xpath("span[@class='_3mfro f-test-text-company-item-location _9fXTd _2JVkc _3e53o']/span[2]/text()").extract_first()
        #print(name)
        yield JobparserItem(name=name, salary=salary, links=links, address=address)