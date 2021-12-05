import scrapy
import os


class ConcordiaSpider(scrapy.Spider):
    """
    go to the top directory path and use  "scrapy crawl concordia -a file_num=2"
    """
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
        path_list = response.request.url.split('/');
        print("URL: " + str(path_list))
        file_path = "files/"
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        for i in range(3, len(path_list) - 1):
            file_path += path_list[i] + "/"
            if not os.path.exists(file_path):
                os.mkdir(file_path)
        if path_list[len(path_list) - 1] == '':
            file_path += "main.html"
        else:
            file_path += path_list[len(path_list) - 1]
        print("file path:   " + file_path)

        f = open(file_path, "w", encoding='utf-8')
        f.write(response.text)
        f.close()
        page_urls = response.css('a::attr(href)').getall()
        for page_url in page_urls:
            if self.file_num <= 0:
                break
            if str(page_url).startswith("/"):
                self.file_num -= 1
                next_page = response.urljoin(page_url)
                yield scrapy.Request(next_page, callback=self.parse)