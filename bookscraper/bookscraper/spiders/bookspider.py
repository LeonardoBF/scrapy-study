import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            yield {
                "title": book.css("h3 > a::attr(title)").get(),
                "price": book.css("p.price_color::text").get(),
                "url": book.css("h3 > a::attr(href)").get(),
            }

        next_pagre_url = response.css('li.next > a::attr(href)').get()
        if next_pagre_url:
            yield scrapy.Request(url=response.urljoin(next_pagre_url), callback=self.parse)