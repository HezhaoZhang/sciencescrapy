# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy

class SciencescrapyPipeline(ImagesPipeline):
    # 重写方法
    def get_media_requests(self, item, info):
        yield scrapy.Request(item["img_url"], meta={'item': item})

    # 指定文件存储路径
    def file_path(self, request, response=None, info=None, *, item=None):
        # 打印图片路径
        # print(request.url)
        # 通过分割图片路径获取图片名字
        img_name = request.meta['item']["issue"] + ".jpg"
        return img_name

    # 返回item对象，给下一执行的管道类
    def item_completed(self, results, item, info):
        # 图片下载路径、url和校验和等信息

        if results[0][0]:
            item['img_name'] = item["issue"] + ".jpg"
            print(results)
            return item
        else:
            pass


class EsPipeline(object):
    def open_spider(self, spider):
        self.es = Elasticsearch(timeout=300, max_retries=100, retry_on_timeout=True)
        self.items = []

    def process_item(self, item, spider):
        if item:
            data = {}
            for k in item:
                if k != 'id':
                    data[k] = item[k]
            data.update(_index='aitopics', _id=item['id'])
            self.items.append(data)
            if len(self.items) == 50:
                helpers.bulk(self.es, self.items)
                self.items = []
            return item
        else:
            pass

    def close(self, spider):
        helpers.bulk(self.es, self.items)