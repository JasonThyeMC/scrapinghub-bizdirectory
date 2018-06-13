# -*- coding: utf-8 -*-
import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    allowed_domains = ['www.ctoscredit.com.my']
    
    # List comprehension to loop from a to z, 2000 is arbitary tested only on the first dozen of alphabets
    start_urls = ['https://www.ctoscredit.com.my/business-directory/%s/%d' %(x,n) for x in alphabets for n in range(1,2000)]
    
    def parse(self, response):
        for bizItem in response.css('li'): # Click into every company link to get more info
            url = bizItem.css('a::attr(href)').extract_first()
            request = scrapy.Request(url, callback=self.parse_details)
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
