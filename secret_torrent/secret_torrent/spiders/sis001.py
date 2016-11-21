# -*- coding: utf-8 -*-
import scrapy
import time
# from scrapy.loader import ItemLoader
from secret_torrent.items import SecretBasicItem, SecretTorrentItem, SecretCommentItem, SecretPictureItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class Sis001Spider(scrapy.Spider):
    name = "sis001"
    allowed_domains = ["sis001.com"]
    start_urls = ['http://www.sis001.com/forum/forum-143-1.html']

    def parse(self, response):
        urls_need = response.xpath('//td[@class="folder"]/a/@href').extract()
        for i in urls_need:
            yield scrapy.Request('http://www.sis001.com/forum/' + i, callback=self.parse_get_torrent)
        if len(urls_need) <= 10:
            front_number = response.url.replace('-', '.', 1).find('-') + 1
            last_number = response.url.find('.html')
            page = int(response.url[front_number:last_number])
            new_url = response.url[:front_number] + \
                str(page + 1) + response.url[last_number:]
            return scrapy.Request(new_url, callback=self.parse)

    def parse_get_torrent(self, response):

        special_value = time.time()
        item_basic = SecretBasicItem()
        torrent = response.xpath(
            '//div[@class="mainbox viewthread"]//div[@class="t_msgfont"]').extract()
        video_verb = ['影片名称', '影片名稱', '主演女优', '影片格式', '影片大小', '影片時間',
                      '是否有码', '下載軟體', '種子限期', '哈希校验', '圖片預覽', '影片预览', ]
        video_number = []
        for i in video_verb:
            if torrent[0].find(i) != -1:
                video_number.append(torrent[0].find(i))
        try:
            video_information = torrent[0][
                min(video_number) - 1:max(video_number) - 1].replace('<br>', '').splitlines()
        except:
            video_information = torrent[0]

        torrent_name = response.xpath(
            '//dl[@class="t_attachlist"]//dt/a/text()').extract()[1]
        torrent_download = response.xpath(
            '//dl[@class="t_attachlist"]//dd/p/text()').extract_first().strip()

        item_basic['video_information'] = video_information
        item_basic['torrent_name'] = torrent_name
        item_basic['torrent_download'] = torrent_download
        item_basic['special_value'] = special_value
        yield item_basic

        item_torrent = SecretTorrentItem()
        item_comment = SecretCommentItem()
        item_picture = SecretPictureItem()

        item_torrent['special_value'] = special_value
        item_comment['special_value'] = special_value
        item_picture['special_value'] = special_value

        torrent_url = 'http://www.sis001.com/forum/' + \
            response.xpath(
                '//dl[@class="t_attachlist"]//dt/a/@href').extract()[1]
        yield scrapy.Request('http://www.sis001.com/forum/' + response.xpath('//dl[@class="t_attachlist"]//dt/a/@href').extract()[1], meta={'item': item_torrent}, callback=self.get_torrent)

        comment = []
        for i in (torrent[1:]):
            comment += i[(i.find('t_msgfont') + 11): -5]
            item_comment['comment'] = i[(i.find('t_msgfont') + 11): -5]

            comment_more = list(set(response.xpath(
                '//div[@class="pages_btns"]//div[@class="pages"]//a/@href').extract()))
            for j in comment_more:
                j = 'http://www.sis001.com/forum/' + j
            item_comment['wait_page'] = comment_more
            if len(item_comment['wait_page']) != 0:
                comment_url = item_comment['wait_page'][0]
                item_comment['wait_page'] = item_comment['wait_page'][1:]
                yield scrapy.Request(comment_url, meta={'item': item_comment}, callback=self.get_more_comment)

        item_picture['picture_url'] = []
        item_picture['wait_to_crawl'] = []
        item_picture['picture'] = []
        torrent_picture = response.xpath(
            '//div[@class="mainbox viewthread"]//div[@class="t_msgfont"]//img/@src').extract()
        for j in torrent_picture:
            if j.find('http') != -1:
                item_picture['picture_url'].append(j)
                item_picture['wait_to_crawl'].append(j)

        if item_picture['wait_to_crawl'] == []:
            yield item_picture
        else:
            picture_url_now = item_picture['wait_to_crawl'][0]
            item_picture['wait_to_crawl'] = item_picture['wait_to_crawl'][1:]
            yield scrapy.Request(picture_url_now, meta={'item': item_picture}, callback=self.get_picture, dont_filter=True, errback=self.errback_httpbin)

    def get_torrent(self, response):
        item_torrent = response.meta['item']
        item_torrent['torrent'] = response.body
        yield item_torrent

    def get_more_comment(self, response):
        item_comment = response.meta['item']
        torrent = response.xpath(
            '//div[@class="mainbox viewthread"]//div[@class="t_msgfont"]').extract()
        comment = []
        for i in torrent:
            comment += i[i.find('t_msgfont') + 11: -5]
        item_comment['comment'] += comment
        if item['wait_page'] == []:
            yield item_comment
        else:
            comment_url = item_comment['wait_page'][0]
            item_comment['wait_page'] = item_comment['wait_page'][1:]
            yield scrapy.Request(comment_url, meta={'item': item_comment}, callback=self.get_more_comment)

    def get_picture(self, response):
        item_picture = response.meta['item']
        item_picture['picture'].append(response.body)
        if item_picture['wait_to_crawl'] == []:
            yield item_picture
        else:
            picture_url_now = item_picture['wait_to_crawl'][0]
            item_picture['wait_to_crawl'] = item_picture['wait_to_crawl'][1:]
            yield scrapy.Request(picture_url_now, meta={'item': item_picture}, callback=self.get_picture, dont_filter=True, errback=self.errback_httpbin)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))


        item_picture = failure.request.meta['item']
        if item_picture['wait_to_crawl'] == []:
            yield item_picture
        else:
            picture_url_now = item_picture['wait_to_crawl'][0]
            item_picture['wait_to_crawl'] = item_picture['wait_to_crawl'][1:]
            yield scrapy.Request(picture_url_now, meta={'item': item_picture}, callback=self.get_picture, dont_filter=True, errback=self.errback_httpbin)

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
