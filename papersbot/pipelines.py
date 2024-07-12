# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline


class PapersbotPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # if spider.name == "semantic":
        #     r = self.db["semantic"].update_one(
        #         {"p_id": item.get("p_id")}, {"$set": dict(item)}, upsert=True
        #     )
        # elif spider.name == "arxiv":
        #     r = self.db["arxiv"].update_one(
        #         {"p_id": item.get("p_id")}, {"$set": dict(item)}, upsert=True
        #     )
        if len(item['file_urls']) == 0:
            return item
        else:
            r = self.db["geoscience"].update_one(
                {"p_id": item.get("p_id")}, {"$set": dict(item)}, upsert=True
            )
            # logging.debug("Article added to MongoDB")
            return item
