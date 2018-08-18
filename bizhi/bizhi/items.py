# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BizhiItem(scrapy.Item):
    # define the fields for your item here like:

    imageType = scrapy.Field()
    imagename = scrapy.Field()
    imageurl = scrapy.Field()
