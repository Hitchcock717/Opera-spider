# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OperaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    op_title = scrapy.Field()
    op_time = scrapy.Field()
    op_link = scrapy.Field()
    op_next_link = scrapy.Field()
    op_content = scrapy.Field()
    op_next_content = scrapy.Field()
    pass
