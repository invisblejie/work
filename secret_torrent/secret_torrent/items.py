# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
#from scrapy.item import Item, Field


class SecretBasicItem(scrapy.Item):
    special_value = scrapy.Field()
    video_information = scrapy.Field()
    torrent_name = scrapy.Field()
    torrent_download = scrapy.Field()
    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({'special_value': self['special_value'], 'torrent_name':self['torrent_name']})


class SecretTorrentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    special_value = scrapy.Field()
    torrent = scrapy.Field()
    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({'special_value': self['special_value']})


class SecretPictureItem(scrapy.Item):
    special_value = scrapy.Field()
    picture = scrapy.Field()
    picture_url = scrapy.Field()
    wait_to_crawl = scrapy.Field()
    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({'special_value': self['special_value']})


class SecretCommentItem(scrapy.Item):
    special_value = scrapy.Field()
    comment = scrapy.Field()
    wait_page = scrapy.Field()
    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({'special_value': self['special_value']})
