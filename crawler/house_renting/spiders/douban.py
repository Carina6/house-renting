# -*- coding: utf-8 -*-
from urllib import parse

from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import Rule, CrawlSpider

from ..items import HouseRentingDoubanItem


class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['douban.com']
    url = 'https://www.douban.com/group/search?start=0&cat=1013&sort=time&'
    url_params = {
        'q': '金运路'
    }
    url_encode = parse.urlencode(url_params)

    start_urls = [url + url_encode]

    rules = (
        Rule(LinkExtractor(allow=r'/group/search?start=\d+&cat=1013&sort=time&' + url_encode,
                           restrict_css=('div#content div.article table', 'div#content div.article div.paginator')),
             follow=True),
        Rule(LinkExtractor(allow=r'/group/topic/\d+/$'), callback='parse_item'),
    )

    def parse_item(self, response):
        selector = Selector(response=response)
        selector.css('div#content div.article div.topic-content')

        item_loader = ItemLoader(item=HouseRentingDoubanItem(), selector=selector, response=response)
        item_loader.add_css(field_name='title', css='table.infobox *::text')
        item_loader.add_css(field_name='title', css='div#content > h1:first-child::text')
        item_loader.add_value(field_name='source', value=self.name)
        item_loader.add_css(field_name='author', css='h3 span.from a::text')
        item_loader.add_css(field_name='image_urls', css='div.topic-content div#link-report img::attr(src)')
        item_loader.add_css(field_name='author_link', css='h3 span.from a::attr(href)')
        item_loader.add_css(field_name='content', css='div.topic-content div#link-report *::text', re=r'\s*(.*)\s*')
        item_loader.add_value(field_name='source_url', value=response.url)
        item_loader.add_css(field_name='publish_time', css='h3 span:last-child::text',
                            re=r'\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*')

        yield item_loader.load_item()
