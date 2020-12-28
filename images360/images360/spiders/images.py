from scrapy import Spider,Request
from urllib.parse import urlencode
import json
from ..items import ImageItem

class ImagesSpider(Spider):
    name = 'images'
    allowed_domains = ['image.so.com']
    # start_urls = ['http://image.so.com/']

    def start_requests(self):
        # https://image.so.com/zjl?ch=photography&sn=60&listtype=new&temp=1
        data = {'ch':'photography','listtype':'new'}
        base_url = 'https://image.so.com/zjl?'
        for page in range(1,self.settings.get('MAX_PAGE')+1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            yield Request(url,self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImageItem()
            item['id'] = image.get('id')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('title')
            item['thumb'] = image.get('qhimg_thumb')
            yield item

