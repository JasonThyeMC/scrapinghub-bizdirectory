# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import logging
logger = logging.getLogger('mycustomlogger')



class BizdirectoryDownloaderMiddleware(RetryMiddleware):
    
    counter = 0
    def process_response(self, request, response, spider):
        logger.info('process_response function processed http code %s', response.status)
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        if response.status == 500:
            BizdirectoryDownloaderMiddleware.counter = BizdirectoryDownloaderMiddleware.counter + 1
        if BizdirectoryDownloaderMiddleware.counter > 6:
            raise CloseSpider('Too Many Error:500')

        return response
