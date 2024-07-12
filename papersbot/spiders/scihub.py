from urllib.parse import urlparse, urlunparse

import pymongo
import scrapy

from papersbot.items import SciHubItem


PROXY = "http://qrzrstsy:9waO7mrv2pVtiStz_country-China@3.219.225.245:31112"
# PROXY = "http://qrzrstsy:9waO7mrv2pVtiStz_country-UnitedStates@3.219.225.245:31112"


class SciHubSpider(scrapy.Spider):
    name = "scihub"
    allowed_domains = ["sci-hub.se"]
    handle_httpstatus_list = []

    def __init__(self, mongo_uri, mongo_db, **kwargs):
        super().__init__(**kwargs)
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[mongo_db]
        self.collection = self.db["semantic"]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
            **kwargs,
        )
        spider._set_crawler(crawler)
        return spider

    def start_requests(self):
        r = self.collection.find({"files": [], "query": "federated learning"})
        for p in r:
            if p["doi"]:
                yield scrapy.Request(
                    url=f"https://sci-hub.se/{p['doi']}",
                    callback=self.parse,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    },
                    # meta={"doi": p["doi"], "p_id": p["p_id"], "proxy": PROXY},
                    meta={"doi": p["doi"], "p_id": p["p_id"]},
                )

    def parse(self, response, **kwargs):
        # TODO: 频率过高时返回 embed 为 None，想办法通过 PROXY 获取 embed，代理下载 pdf
        embed = response.css("#pdf::attr(src)").get()
        o = urlparse(embed)
        try:
            pdf_url = urlunparse(("https", o.netloc, o.path, "", "", ""))
        except TypeError:
            self.logger.debug(f"embed: {embed}")
            return
        scihub_item = SciHubItem(
            p_id=response.meta["p_id"],
            doi=response.meta["doi"],
            pdf_url=pdf_url,
            file_urls=[pdf_url],
        )
        yield scihub_item
