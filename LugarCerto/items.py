# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item


class LugarCertoItem(Item):
    titulo = scrapy.Field()
    endereco = scrapy.Field()
    preco = scrapy.Field()
    anunciante = scrapy.Field()
