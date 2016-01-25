# -*- coding: utf-8 -*-
import json
from urlparse import urljoin

from scrapy import Spider
from scrapy.http import Request

from craiglist_us.items import CraiglistUsItem


class CraiglistSpider(Spider):
    name = "craiglist"
    allowed_domains = ["craigslist.org"]
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
        for city in area_json[:2]:
            if city.get('hostname'):
                url = 'http://%s.craigslist.org/search/rts' % city.get('hostname')
                yield Request(url=url, callback=self.parse_links)

    def parse_links(self, response):
        LINKS_XPATH = '//span[@class="rows"]/p[@class="row"]/a/@href'
        NEXT_PAGE_XPATH = '//a[@class="button next"]/@href'

        links = response.xpath(LINKS_XPATH).extract()
        # if no links are present exit from the function
        if links:
            for link in links:
                # converting the relative url to absolute url
                url = urljoin(self.base_url, link)
                yield Request(url=url,
                              callback=self.parse_data
                              )
        else:
            return

        # pagination
        next_page = response.xpath(NEXT_PAGE_XPATH).extract()
        if next_page:
            next_page_url = urljoin(self.base_url, next_page[0])
            yield Request(url=next_page_url,
                          callback=self.parse_links
                          )

    def parse_data(self, response):
        """
        Extract the data from the details page
        """
        # XPATHS SECTION
        TITLE_XPATH = '//span[@class="postingtitletext"]/text()'
        DESCRIPTION_XAPTH = '//section[@id="postingbody"]//text()'
        POST_ID_XPATH = '//p[@class="postinginfo" and contains(text(), "post id:")]/text()'
        POSTED_DATE_XPATH = '//p[@class="postinginfo reveal" and contains(text(), "posted: ")]/time/text()'
        POST_UPDATED_DATE_XPATH = '//p[@class="postinginfo reveal" and contains(text(), "updated: ")]/time/text()'
        LATITUDE_XPATH = '//div[@id="map"]/@data-latitude'
        LONGITUDE_XPATH = '//div[@id="map"]/@data-longitude'
        CATEGORIES_XPATH = '//ul[@class="breadcrumbs"]/li/a/text()'

        # DATA EXTRACTION
        title = response.xpath(TITLE_XPATH).extract()
        description = response.xpath(DESCRIPTION_XAPTH).extract()
        post_id = response.xpath(POST_ID_XPATH).extract()
        posted_on = response.xpath(POSTED_DATE_XPATH).extract()
        posted_updated_on = response.xpath(POST_UPDATED_DATE_XPATH).extract()
        latitude = response.xpath(LATITUDE_XPATH).extract()
        longitude = response.xpath(LONGITUDE_XPATH).extract()
        categories = response.xpath(CATEGORIES_XPATH).extract()

        # CLEANING THE DATA
        title = ' '.join(' '.join(title).split()) if title else ''
        description = ' '.join(' '.join(description).split()) if title else ''
        post_id = post_id[0].strip().replace(
            'post id:', '').strip() if post_id else ''
        posted_on = posted_on[0].strip() if posted_on else ''
        posted_updated_on = posted_updated_on[
            0].strip() if posted_updated_on else ''
        latitude = latitude[0].strip() if latitude else ''
        longitude = longitude[0].strip() if longitude else ''
        categories = [category.strip()
                      for category in categories if category.strip()] if categories else []
        # post details
        post = {'id': post_id,
                'posted_on': posted_on,
                'updated_on': posted_updated_on
                }
        # geo details
        geo = {'latitude': latitude, 'longitude': longitude}
        # create item class object
        item = CraiglistUsItem(
                                title=title,
                                description=description,
                                post=post,
                                geo=geo,
                                categories=categories,
                                url=response.url
                            )
        yield item
