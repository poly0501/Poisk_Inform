# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&st=searchVacancy&text=python']
    #start_urls = ['https: // hh.ru / search / vacancy?L_is_autosearch = false & clusters = true & enable_snippets = true & text = Python & page = 1']

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback = self.parse)

        vacancy = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@class=\'header\']//span/text()").extract_first()
        #salary = response.css('div.vacancy-title p.vacancy-title-salary::text').extract()
        salary = response.xpath("//div[@class='vacancy-serp-item__compensation']//text()").extract_first()
        links = response.xpath("//div[@class='resume-search-item__name']/span[1]/a[@class='bloko-link HH-LinkModifier']/@href").extract_first()
        #links = response.css("a.bloko-link a.HH-LinkModifier::attr(href)").extract()
        address = response.xpath("//span[@data-qa='vacancy-serp__vacancy-address']//text()").extract_first()
        #address = response.css("span.vacancy-serp__vacancy-address::text").extract_first()

        #print(name, salary, address, links)
        yield JobparserItem(name=name, salary=salary, links=links, address=address)
