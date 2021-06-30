import scrapy
from sciencescrapy.items import SciencescrapyItem

class ScienceSpider(scrapy.Spider):
    name = 'science'
    allowed_domains = ['science.sciencemag.org/']
    start_urls = ["https://science.sciencemag.org//"]

    def start_requests(self):
        for i in range(2020, 1979, -1):
            url = "https://science.sciencemag.org/content/by/year/" + str(i)
            item = SciencescrapyItem()
            item["year"] = str(i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"item":item})

    def parse(self, response):
        for i in response.xpath("//ul[@class='issue-month-detail']/li"):
            url = response.urljoin(i.xpath(".//a/@href")[0].extract())
            item = response.meta["item"]
            item["date"] = i.xpath("./div/div/a/h3/text()")[0].extract()
            item["vol"] = url.split("/")[-2]
            item["issue"] = url.split("/")[-1]
            yield scrapy.Request(url=url, callback=self.second_parse, dont_filter=True, meta={"item":item})

    def second_parse(self, response):
        about_cover = response.xpath("//div[@class='panel-pane pane-highwire-markup box-standout "
                                     "priority-2']/div/div/div")
        item = response.meta["item"]
        summary = about_cover.xpath(".//div[@class='caption cover-img']").xpath("string(.)").extract()[0]
        img = about_cover.xpath("./img/@src").extract()[0]
        item["summary"] = summary
        item["img"] = img
        yield item