# -*- coding: utf-8 -*-
import scrapy


class CraigslistSpider(scrapy.Spider):
    name = "craigslist"
    allowed_domains = ["cragslist.org"]
    start_urls = (
        'http://www.cragslist.org/',
    )

    def parse(self, response):
        pass
