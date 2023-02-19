from scrapy import Spider

class BookScraping(Spider):

    name  = 'book_bot' # name of spider
    start_urls = []  # url to start with
    def parse(self, response, **kwargs):
        return super().parse(response, **kwargs)