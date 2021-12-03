import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self, test=None, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # for quote in response.css('div.quote'):
        #     yield {
        #         'text': quote.css('span.text::text').get(),
        #         'author': quote.css('small.author::text').get(),
        #         'tags': quote.css('div.tags a.tag::text').getall(),
        #     }
        item = response.css('a::attr(href)').extract()
        print(str(item) + "1111111111111111111111111111111111")
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)