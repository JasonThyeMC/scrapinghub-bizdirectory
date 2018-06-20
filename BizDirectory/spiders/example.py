# -*- coding: utf-8 -*-
import scrapy
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class ExampleSpider(scrapy.Spider):
    name = 'example'
#    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    alphabets = 'z'
    pages = [1951,1150,1279,837,991,681,1029,891,828,626,1187,855,1865,692,380,1754,116,831,2790,1540,385,373,620,51,324,205]
    allowed_domains = ['www.ctoscredit.com.my']
    
    # List comprehension to loop from a to z, 2000 is arbitary tested only on the first dozen of alphabets
    start_urls = ['https://www.ctoscredit.com.my/business-directory/%s/%d' %(x,n) for x in alphabets for n in range(1,205)]
#    start_urls = ['https://www.ctoscredit.com.my/business-directory/%s/%d' %(x,n) for x in alphabets for n in range(1,4)]

    def parse(self, response):
#        links = [bizItem.css('a::attr(href)').extract_first() for bizItem in response.css('li')]
#        parallelProcess(links)
        for bizItem in response.css('li'): # Click into every company link to get more info
            request = scrapy.Request(bizItem.css('a::attr(href)').extract_first(), callback=self.parse_details)
            yield request
    
    def parse_details(self, response): # Process after company details page fully loaded
        companyInfo = {} # Store key-value pair where key will be column name in the final table
        for details in response.css('tr'): # Extract only the table from the company details page
            info = details.css('td::text').extract() # Process the table row by row
            if len(info) < 2: # Some row consists missing value
                companyInfo[info[0]] = None # Replace the value with null
            else:
                companyInfo[info[0]] = info[1] # Represent one column in the final table
        yield companyInfo # Populate row of final table one column at a time
                
    def handle_spider_closed(spider, reason):
        print('Work time:', spider.crawler.stats.get_value('finish_time') - spider.crawler.stats.get_value('start_time'))


    dispatcher.connect(handle_spider_closed, signals.spider_closed)

