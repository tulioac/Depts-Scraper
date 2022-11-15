import scrapy

from .utils.DataExtractor import DataExtractor


class QuotesSpider(scrapy.Spider):
    name = "deputadas"

    def start_requests(self):

        deps_file = open("lista_deputadas.txt", "r")

        deps_urls = deps_file.read().splitlines()

        for url in deps_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data_extractor = DataExtractor(response)

        dep_data = data_extractor.run(gender="F")

        yield dep_data
