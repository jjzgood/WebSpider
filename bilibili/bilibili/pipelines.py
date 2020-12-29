from datetime import datetime
import pymongo

from .spiders.uploader import UploaderSpider

class DatetimeStrfPipeline:
    """格式化时间戳为字符串"""
    def process_item(self, item, spider):
        if item['created']:
            item['created'] = datetime.fromtimestamp(item['created']).strftime('%Y-%m-%d %H:%M:%S')
            return item


class DescriptionStrfPipeline:
    """替换description中的\n"""
    def process_item(self, item, spider):
        if item['description']:
            item['description'] = item['description'].replace('\n','')
            return item


class MongoPipeline:
    """保存到mongo"""
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = UploaderSpider.uploader
        self.db[name].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()

