# -*- coding: utf-8 -*-
import scrapy
import re
import copy
from Opera.items import OperaItem


class OperaSpider(scrapy.Spider):
    name = 'opera'
    # allowed_domains = ['http://xiqu.chnart.com']
    start_urls = ['http://xiqu.chnart.com/index.php?m=content&c=index&a=lists&catid=33/']

    main_url = 'http://xiqu.chnart.com/'

    def parse(self, response):
        print(response)
        rd = OperaItem()

        raw_link = response.xpath('//div[@id="pages"]/a[6]/@href').extract_first()

        next_link = self.main_url + raw_link
        rd['op_next_link'] = next_link
        yield scrapy.http.Request(url=next_link,
                                  callback=self.parse,
                                  dont_filter=False)

        op_titles = response.xpath('//ul[@class="list lh24 f14"]/li/a/text()').extract()

        op_times = response.xpath('//ul[@class="list lh24 f14"]/li/span/text()').extract()

        op_links = response.xpath('//ul[@class="list lh24 f14"]/li/a/@href').extract()

        for title, time, link in zip(op_titles, op_times, op_links):
            new_title = re.sub('.*《', "", title)
            rd['op_title'] = re.sub('》.*', "", new_title)
            rd['op_time'] = time
            rd['op_link'] = link
            yield scrapy.http.Request(url=link,
                                      meta={'key': copy.deepcopy(rd)},
                                      callback=self.detail)

    def detail(self, response):
        rd = response.meta['key']

        content = response.xpath('//td[@style]/p/text()').extract()
        if content:
            content1 = [con.strip() for con in content]
            content2 = ''.join(content1).split()
            rd['op_content'] = ''.join(content2)
        else:
            new_content = response.xpath('//td[@style]/div/text()').extract()
            content1 = [con.strip() for con in new_content]
            content2 = ''.join(content1).split()
            rd['op_content'] = ''.join(content2)

        nextpage_links = response.xpath('//div[@id="pages"]/a/@href').extract()

        if nextpage_links:
            if response.xpath('//dic[@id="pages"]/span/text()').extract():
                rd['op_next_content'] = ''
                yield rd
            else:
                for link in nextpage_links:
                    yield scrapy.http.Request(url=link,
                                              meta={'key-child': copy.deepcopy(rd)},
                                              callback=self.nextpage)
        else:
            rd['op_next_content'] = ''
            yield rd

    def nextpage(self, response):
        rd = response.meta['key-child']

        content = response.xpath('//td[@style]/p/text()').extract()
        if content:
            content1 = [con.strip() for con in content]
            content2 = ''.join(content1).split()
            rd['op_next_content'] = ''.join(content2)
        else:
            new_content = response.xpath('//td[@style]/div/text()').extract()
            content1 = [con.strip() for con in new_content]
            content2 = ''.join(content1).split()
            rd['op_next_content'] = ''.join(content2)
        yield rd







