import scrapy


class CrossrefSpider(scrapy.Spider):
    name = 'crossref'
    allowed_domains = ['crossref.org']
    start_urls = ['https://api.crossref.org/works?query=sedimentary+rock&filter=has-abstract:true&select=title,DOI,abstract,author,subject,created&cursor=*&rows=50&mailto=apps@grwa.ng']

    def parse(self, response):
        pass
