# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PapersbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SemanticItem(scrapy.Item):
    p_id = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    authors = scrapy.Field()
    fields_of_study = scrapy.Field()
    doi = scrapy.Field()
    pdf_url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    query = scrapy.Field()
    topic = scrapy.Field()


class ArxivItem(scrapy.Item):
    p_id = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    pdf_url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    query = scrapy.Field()
    doi = scrapy.Field()
    topic = scrapy.Field()
    authors = scrapy.Field()
    fields_of_study = scrapy.Field()


class SciHubItem(scrapy.Item):
    p_id = scrapy.Field()
    doi = scrapy.Field()
    pdf_url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
