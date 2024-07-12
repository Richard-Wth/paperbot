import scrapy
from datetime import datetime
from urllib import parse
import json
from papersbot.items import ArxivItem

PROXY = (
    "http://leonwong:zoKi2wfkbA8gnx6p_country-UnitedStates@proxy.packetstream.io:31112"
)


class ArxivSpider(scrapy.Spider):
    name = "arxiv"
    allowed_domains = ["arxiv.org"]
    handle_httpstatus_list = []

    def get_keywords(self):
        with open("/home/wgr/papersbot/assets/地学/keywords.json", "r") as f:
            keywords = json.load(f)
        return keywords

    def start_requests(self):
        keywords = self.get_keywords()
        for topic in keywords.keys():
            queries = keywords[topic]
            for query in queries:
                payload = {
                    "query": query,
                    "searchtype": "all",
                    "source": "header",
                }
                yield scrapy.Request(
                    url="https://arxiv.org/search/?" + parse.urlencode(payload),
                    method="GET",
                    callback=self.parse,
                    meta={"proxy": PROXY},
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    },
                    cb_kwargs={"payload": payload, "topic": topic},
                )
        # queries = [
        #     "federated learning",
        # ]

        # for query in queries:
        #     payload = {
        #         "query": query,
        #         "searchtype": "all",
        #         "source": "header",
        #     }
        #     yield scrapy.Request(
        #         url="https://arxiv.org/search/?" + parse.urlencode(payload),
        #         method="GET",
        #         callback=self.parse,
        #         meta={"proxy": PROXY},
        #         headers={
        #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        #         },
        #         cb_kwargs={"payload": payload},
        #     )

    def parse(self, response, payload, topic=""):
        info_nodes = response.css(".arxiv-result")
        for result in info_nodes:
            info_url = result.css(".list-title > a").attrib["href"]
            title = result.css(".title").xpath("string(.)").get().strip()
            a_less = result.css(".abstract-full a")[0].root
            a_less.getparent().remove(a_less)
            abstract = result.css(".abstract-full").xpath("string(.)").get().strip()
            p_id = info_url.rsplit("/", 1)[1]
            pdf_url = "https://arxiv.org/pdf/" + p_id
            doi = result.css(".is-marginless div:last-child a::text").get("")
            authors = []
            author_nodes = result.css(".authors > a")
            for author_node in author_nodes:
                authors.append(author_node.css("::text").get())
            fields_of_study = []
            fields_nodes = result.css(".tags.is-inline-block .tag")
            for field_node in fields_nodes:
                fields_of_study.append(field_node.attrib["data-tooltip"])
            paper_item = ArxivItem(
                p_id=p_id,
                title=title,
                abstract=abstract,
                pdf_url=pdf_url,
                file_urls=[pdf_url],
                query=payload["query"],
                authors=authors,
                fields_of_study=fields_of_study,
                doi=doi,
                topic=topic,
            )
            yield paper_item

        try:
            next_page = response.css("a.pagination-next")[0].attrib.get("href", None)
        except IndexError:
            next_page = None
        if next_page is not None:
            yield scrapy.Request(
                url="https://arxiv.org" + next_page,
                method="GET",
                callback=self.parse,
                meta={"proxy": PROXY},
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                },
                cb_kwargs={"payload": payload},
            )
