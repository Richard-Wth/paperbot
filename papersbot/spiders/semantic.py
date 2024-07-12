import json
import os
from datetime import datetime

import scrapy
from papersbot.items import SemanticItem

PROXY = (
    "http://leonwong:zoKi2wfkbA8gnx6p_country-UnitedStates@proxy.packetstream.io:31112"
)


class SemanticSpider(scrapy.Spider):
    name = "semantic"
    allowed_domains = ["semanticscholar.org"]
    handle_httpstatus_list = []
    ignore_fields = [
        "Medicine",
        "Economics",
        "Business",
        "Poliitical Science",
        "Education",
        "Sociology",
        "Art",
        "History",
        "Philosophy",
        "Linguistics",
        "Law",
    ]
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

    def get_keywords(self):
        with open("/home/wgr/papersbot/assets/地学/keywords.json", "r") as f:
            keywords = json.load(f)
        return keywords

    def start_requests(self):
        keywords = self.get_keywords()
        topic = self.topic
        queries = keywords[topic]
        for query in queries:
            payload = {
                "queryString": query,
                "page": 1,
                "pageSize": 10,
                "sort": "relevance",
                "authors": [],
                "coAuthors": [],
                "venues": [],
                "yearFilter": None,
                "requireViewablePdf": True,
                "publicationTypes": [],
                "externalContentTypes": [],
                "fieldsOfStudy": [],
                "useFallbackRankerService": False,
                "useFallbackSearchCluster": False,
                "hydrateWithDdb": True,
                "includeTldrs": True,
                "performTitleMatch": True,
                "includeBadges": True,
                "tldrModelVersion": "v2.0.0",
                "getQuerySuggestions": False,
            }
            yield scrapy.Request(
                url="https://www.semanticscholar.org/api/1/search",
                method="POST",
                callback=self.parse,
                meta={"proxy": PROXY},
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                },
                body=json.dumps(payload),
                cb_kwargs={"payload": payload, "topic": topic},
            )

    # def start_requests(self):
    #     queries = [
    #         "federated learning",
    #     ]

    #     for query in queries:
    #         payload = {
    #             "queryString": query,
    #             "page": 1,
    #             "pageSize": 10,
    #             "sort": "relevance",
    #             "authors": [],
    #             "coAuthors": [],
    #             "venues": [],
    #             "yearFilter": None,
    #             "requireViewablePdf": True,
    #             "publicationTypes": [],
    #             "externalContentTypes": [],
    #             "fieldsOfStudy": [],
    #             "useFallbackRankerService": False,
    #             "useFallbackSearchCluster": False,
    #             "hydrateWithDdb": True,
    #             "includeTldrs": True,
    #             "performTitleMatch": True,
    #             "includeBadges": True,
    #             "tldrModelVersion": "v2.0.0",
    #             "getQuerySuggestions": False,
    #         }
    #         yield scrapy.Request(
    #             url="https://www.semanticscholar.org/api/1/search",
    #             method="POST",
    #             callback=self.parse,
    #             meta={"proxy": PROXY},
    #             headers={
    #                 "Content-Type": "application/json",
    #                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    #             },
    #             body=json.dumps(payload),
    #             cb_kwargs={"payload": payload},
    #         )

    def parse(self, response, payload, topic=""):
        response_dict = json.loads(response.body)
        total_page = response_dict["totalPages"]
        results = response_dict["results"]
        for paper in results:
            p_id = paper["id"]
            corpus_id = paper["corpusId"]
            title = paper["title"]["text"]
            abstract = paper["paperAbstract"]["text"]
            authors = [author[0]["name"] for author in paper["authors"]]
            venue = paper["venue"]["text"]
            fields_of_study = paper["fieldsOfStudy"]
            doi = paper["doiInfo"]["doi"] if paper.get("doiInfo") else None
            citation = (
                0
                if len(paper["scorecardStats"]) == 0
                else paper["scorecardStats"][0]["citationCount"]
            )
            pub_date = (
                datetime.strptime(paper["pubDate"], "%Y-%m-%d")
                if paper.get("pubDate")
                else None
            )
            try:
                pdf_url = paper["alternatePaperLinks"][0]["url"]
            except IndexError:
                self.logger.debug(
                    f"IndexError in query {payload['queryString']} page {payload['page']}"
                )
                try:
                    pdf_url = paper["primaryPaperLink"]["url"]
                except KeyError:
                    self.logger.debug(
                        f"KeyError in query {payload['queryString']} page {payload['page']}"
                    )
                    continue
            if any(x in self.ignore_fields for x in fields_of_study):
                paper_item = SemanticItem(
                    p_id=p_id,
                    title=title,
                    abstract=abstract,
                    authors=authors,
                    fields_of_study=fields_of_study,
                    doi=doi,
                    pdf_url=pdf_url,
                    file_urls=[],
                    query=payload["queryString"],
                    topic=topic,
                )
            else:
                paper_item = SemanticItem(
                    p_id=p_id,
                    title=title,
                    abstract=abstract,
                    authors=authors,
                    fields_of_study=fields_of_study,
                    doi=doi,
                    pdf_url=pdf_url,
                    file_urls=[pdf_url],
                    query=payload["queryString"],
                    topic=topic,
                )

            yield paper_item

        if response_dict["query"]["page"] < total_page:
            response_dict["query"]["page"] += 1
            yield scrapy.Request(
                url="https://www.semanticscholar.org/api/1/search",
                method="POST",
                callback=self.parse,
                meta={"proxy": PROXY},
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                },
                body=json.dumps(response_dict["query"]),
                cb_kwargs={"payload": response_dict["query"], "topic": topic},
            )
