from scrapy import Spider
from book_scraping.items import BookScrapingItem
from scrapy.selector import Selector


class BookScraping(Spider):

    name  = 'book_bot' # name of spider
    start_urls = ["https://www.amazon.in/s?i=stripbooks&bbn=976389031&rh=n%3A976389031%2Cp_n_publication_date%3A2684819031&dc&page=1&qid=1676798077&rnid=2684818031&ref=sr_pg_1"]  # url to start with

    # page_number
    page_number = 2

    def parse(self, response, **kwargs):

        # instance of items.py class
        items = BookScrapingItem()

        all_div_books = response.xpath("//div[@class='a-section']").extract()

        for book in all_div_books:
            # starting the scraping
            book_names = book.css('.a-size-medium::text').extract()
            # book_names = book.xpath("//span[@class=a-size-medium]/text()").extract()

            book_price = book.css('.a-price-fraction , .a-price-whole').css('::text').extract()
            # book_price = book.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "a-price-fraction", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "a-price-whole", " " ))]').xpath('text()').extract()
            
            book_author = book.css('.a-color-secondary .a-size-base+ .a-size-base , .a-color-secondary .a-size-base.s-link-style').css('::text').extract()
            # book_author = book.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "a-color-secondary", " " ))]//*+[contains(concat( " ", @class, " " ), concat( " ", "a-size-base", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "a-size-base", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "a-color-secondary", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "a-size-base", " " )) and contains(concat( " ", @class, " " ), concat( " ", "s-link-style", " " ))]').xpath('/text()').extarct()

            book_image = book.css('.s-image::attr(src)').extract()
            # book_image = book.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "s-image", " " ))]').xpath('@src').extract()

            items['product_price'] = book_price
            items['product_author'] = book_author
            items['product_name'] = book_names
            items['product_imagelink'] = book_image

            yield items

        # pagination
        next_page = "https://www.amazon.in/s?i=stripbooks&bbn=976389031&rh=n%3A976389031%2Cp_n_publication_date%3A2684819031&dc&page={}&qid=1676798077&rnid=2684818031&ref=sr_pg_{}".format(BookScraping.page_number, BookScraping.page_number)

        if BookScraping.page_number <= 49:
            BookScraping.page_number += 1
        yield response.follow(next_page, callback = self.parse)

