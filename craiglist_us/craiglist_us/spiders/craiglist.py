# -*- coding: utf-8 -*-
import json
from urlparse import urljoin

from scrapy import Spider
from scrapy.http import Request


class CraiglistSpider(Spider):
    name = "craiglist"
    allowed_domains = ["craiglist.org"]
    start_urls = (
        'http://www.craigslist.org/about/areas.json',
    )
    base_url = 'http://www.craigslist.org'

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
        # url format : CITYNAME.craiglist.org
        for city in area_json:
            if city.get('hostname'):
                url = '%s.craigslist.org' % city.get('hostname')
                yield Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        # base xpath for category links and text
        CATEGORIES_BASE_XPATH = '//div[@id="bbb"]/div[@class="cats"]/ul/li/a'
        for link in response.xpath(CATEGORIES_BASE_XPATH):
            # category_text is passed along with the url as meta_data in
            # request
            meta_data = {}
            # category url, need to append base url
            url = link.xpath('./@href').extract()
            if url:
                # converting the relative url to absolute url
                url = urljoin(self.base_url, url[0])
                # catgeory_name
                url_text = link.xpath('./span/text()').extract()
                url_text = url_text[0].strip() if url_text else ''
                meta_data = {'category': url_text}
                yield Request(url=url,
                              callback=self.parse_links,
                              meta=meta_data
                              )

    def parse_links(self, response):
        NEXT_PAGE_XPATH = '//a[@class="button next"]/@href'

        next_page = response.xpath(NEXT_PAGE_XPATH).extract()
        if next_page:
            next_page_url = urljoin(self.base_url, next_page[0])
            yield Request(url=next_page_url,
                          callback=self.parse_links
                          )
