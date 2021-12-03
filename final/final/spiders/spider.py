import scrapy
from bs4 import BeautifulSoup


class ConcordiaSpider(scrapy.Spider):
    name = "concordia"
    file_num = 0

    def __init__(self, file_num=None, *args, **kwargs):
        self.file_num = int(file_num)
        print("The number of crawled files is " + file_num)
        super(ConcordiaSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        urls = [
            'https://www.concordia.ca/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("URL: " + response.request.url)
        soup = BeautifulSoup(response.text)
        print(soup.get_text())
        f = open("example.txt", "w", encoding='utf-8')
        f.write(soup.get_text())
        f.close()
        page_urls = response.css('a::attr(href)').getall()
        for page_url in page_urls:
            if self.file_num <= 0:
                break
            if str(page_url).startswith("/"):
                self.file_num -= 1
                next_page = response.urljoin(page_url)
                print(next_page)
                yield scrapy.Request(next_page, callback=self.parse)