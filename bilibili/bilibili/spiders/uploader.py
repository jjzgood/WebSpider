from scrapy import Spider,Request
from urllib.parse import urlencode
import json
from ..items import UploaderItem


class UploaderSpider(Spider):
    name = 'uploader'
    allowed_domains = ['bilibili.com']
    # start_urls = ['http://bilibili.com/']
    uploader = 'chineseboy'

    def start_requests(self):
        # https://api.bilibili.com/x/space/arc/search?mid=390461123&ps=30&tid=0&pn=23&keyword=&order=pubdate&jsonp=jsonp
        # up主ID：中国boy
        up_id = '562197'
        data = {'mid':up_id,'ps':30,'tid':0,'order':'pubdate','jsonp':'jsonp'}
        max_page = 47
        base_url = 'https://api.bilibili.com/x/space/arc/search?'
        for page in range(1,max_page+1):
            data['pn'] = page
            params = urlencode(data)
            url = base_url+params
            yield Request(url,self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        result_vlist = result.get('data').get('list').get('vlist')
        for play_info in result_vlist:
            item = UploaderItem()
            item['bvid'] = play_info.get('bvid')
            item['title'] = play_info.get('title')
            item['description'] = play_info.get('description')
            item['play'] = play_info.get('play')
            item['comment'] = play_info.get('comment')
            item['created'] = play_info.get('created')
            yield item
