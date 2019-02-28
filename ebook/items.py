# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EbookItem(scrapy.Item):
    # define the fields for your item here like:

    # 章名
    chapter = scrapy.Field()

    # 节名
    section = scrapy.Field()

    # 页面链接
    pages = scrapy.Field()
