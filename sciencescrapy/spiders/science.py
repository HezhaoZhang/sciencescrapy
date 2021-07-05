import scrapy
from sciencescrapy.items import SciencescrapyItem


class ScienceSpider(scrapy.Spider):
    name = 'science'
    allowed_domains = ['science.sciencemag.org/']
    start_urls = ["https://science.sciencemag.org//"]

    def start_requests(self):
        for i in range(2020, 1979, -1):
            url = "https://science.sciencemag.org/content/by/year/" + str(i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        for i in response.xpath("//ul[@class='issue-month-detail']/li"):
            url = response.urljoin(i.xpath(".//a/@href")[0].extract())
            yield scrapy.Request(url=url, callback=self.second_parse, dont_filter=True)

    def second_parse(self, response):
        about_cover = response.xpath("//div[@class='panel-pane pane-highwire-markup box-standout "
                                     "priority-2']/div/div/div")
        item = SciencescrapyItem()
        metadata = response.xpath("//div[@class='panel-pane pane-panels-mini pane-jnl-sci-art-issue box-standout "
                                  "priority-2']//article/div[@class='media__body']")
        item['vol'] = metadata.xpath("./p/text()").extract()[0]
        item['date'] = metadata.xpath("./p/text()").extract()[1]
        summary = about_cover.xpath(".//div[@class='caption cover-img']").xpath("string(.)").extract()[0]
        img = about_cover.xpath("./img/@src").extract()[0]
        item["summary"] = summary
        item["img_url"] = img
        yield item
