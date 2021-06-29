import scrapy


class ScienceSpider(scrapy.Spider):
    name = 'science'
    allowed_domains = ['science.sciencemag.org/']
    start_urls = ["https://science.sciencemag.org//"]

    def start_requests(self):
        for i in range(2020, 1979, -1):
            url = "https://science.sciencemag.org/content/by/year/" + str(i)
            year = i
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        for i in response.xpath("//ul[@class='issue-month-detail']/li"):
            url = response.urljoin(i.xpath(".//a/@href")[0].extract())
            date = i.xpath("./div/div/a/h3/text()")[0].extract()
            yield scrapy.Request(url=url, callback=self.second_parse, dont_filter=True)

    def second_parse(self, response):
        about_cover = response.xpath("//div[@class='panel-pane pane-highwire-markup box-standout "
                                     "priority-2']/div/div/div")
        pass