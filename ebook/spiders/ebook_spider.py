# -*- coding: utf-8 -*-
import scrapy
import re
from ebook.items import EbookItem


class EbookSpiderSpider(scrapy.Spider):
    # spider 名称
    name = 'ebook_spider'
    # 允许爬取的域名列表
    allowed_domains = ['www.wsbedu.com', 'dzkbw.com']
    # 爬虫入口网址
    start_urls = ['http://www.dzkbw.com/books/rjb/wuli/xc8s/']

    def parse(self, response):
        """"
        解析目录的每一个章节
        """
        chapter_name = ""

        # 提取章节元素对象
        eles = response.xpath("//div[@class='bookmulu']//a")

        for ele in eles:
            section_name = ""
            name = ""
            link = ""

            # 提取跳转链接
            link = ele.xpath("./@href").extract_first()

            # 提取章节名称
            name = ele.xpath("./text()").extract_first()
            if not name:
                name = ele.xpath(".//b/text()").extract_first()

            # 判断是章还是节
            if re.search('第.章', name) or not re.search('第.节', name):
                chapter_name = name
            else:
                section_name = name

            # 进入每一节链接的页面继续爬
            if not re.search('第.章', name):
                request = scrapy.Request("http://www.dzkbw.com" + link, callback=self.parse_link)
                request.meta['chapterName'] = chapter_name
                request.meta['sectionName'] = section_name
                yield request

    def parse_link(self, response):
        """
        解析节跳转链接
        """
        # 提取跳转链接
        link = response.xpath("//div[@class='bookimg']//a[2]/@href").extract_first()

        # 进入链接的页面继续爬
        request = scrapy.Request("http://www.dzkbw.com" + link, callback=self.parse_pages)
        request.meta['chapterName'] = response.meta['chapterName']
        request.meta['sectionName'] = response.meta['sectionName']
        yield request

    def parse_pages(self, response):
        """
        解析电子书页面图片
        """
        # 收集信息
        item = EbookItem()
        item['chapter'] = response.meta['chapterName']
        item['section'] = response.meta['sectionName']
        item['pages'] = response.xpath("//div[@class='main_left2']//img/@src").extract()
        yield item

        # 提取页码信息和下一页的跳转链接
        page_info = ""
        temp = response.xpath("//td//div[@class='STYLE8']//font/text()").extract()
        for txt in temp:
            page_info += txt.strip().replace('\u3000', '')
        next_link = response.xpath("//div[@class='STYLE8']//font//a[1]/@href").extract_first().replace(' ', '')
        total_page = int(page_info[4:5])
        next_page = int(next_link[-1:])

        # 如果下一页的页码不超过总页数，则继续爬下一页
        if next_page <= total_page:
            request = scrapy.Request("http://www.wsbedu.com/wu51/" + next_link, callback=self.parse_pages)
            request.meta['chapterName'] = response.meta['chapterName']
            request.meta['sectionName'] = response.meta['sectionName']
            yield request