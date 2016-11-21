# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymongo


class SecretTorrentPipeline(object):
    def process_item(self, item, spider):
        return item

# class DuplicatesPipeLine(object):

# def __init__(self):
##		self.ids_seen = set()

# def process_item(self, item, spider):
# if item['hash'] in self.ids_seen:
##			raise DropItem('Duplicate item found: %s' %item)

# else:
# self.ids_seen.add(item['hash'])
# return item


class MongoPipeline(object):

    collection_name = 'scrapy_sis001'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if self.db[self.collection_name].find({'special_value': item['special_value']}).count() == 0:
            self.db[self.collection_name].insert(
                {'special_value': item['special_value']})
        verb = ['video_information', 'torrent_name', 'torrent_download',
                'torrent', 'picture', 'picture_url', 'comment', ]
        wait_to_insert = {}
        for i in item:
            if i in verb:
                wait_to_insert[i] = item[i]
        self.db[self.collection_name].update(
            {'special_value': item['special_value']}, {"$set": wait_to_insert},)
        return item
