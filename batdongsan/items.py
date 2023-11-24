# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BatdongsanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Price = scrapy.Field()
    Area = scrapy.Field()
    BedRoom = scrapy.Field()
    WC = scrapy.Field()
    # pháp lý
    Legal = scrapy.Field()
    Name = scrapy.Field()
    DateUpLoad = scrapy.Field()
    DateExpiration = scrapy.Field()
    Code = scrapy.Field()

