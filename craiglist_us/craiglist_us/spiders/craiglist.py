# -*- coding: utf-8 -*-
import json

from scrapy import Spider
from scrapy.http import Request


class CraiglistSpider(Spider):
    name = "craiglist"
    allowed_domains = ["craiglist.org"]
    start_urls = (
        'http://www.craigslist.org/about/areas.json',
    )

    def parse(self, response):
        """
        Create city-wise url from the json response
        Sample json: {
                     "country":"US",
                     "lat":"37.500000",
                     "lon":"-122.250000",
                     "region":"CA",
                     "name":"SF bay area",
                     "hostname":"sfbay"
                     }
        """
        area_json = {}
        try:
            area_json = json.loads(response.body)
        except Exception, e:
            raise e
        # url format : CITYNAME.craiglist.com
        for city in area_json:
            if city.get('hostname'):
                url = '%s.craigslist.org' % city.get('hostname')
                yield Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        pass
