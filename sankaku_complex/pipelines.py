# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class SankakuComplexTitlePipeline:
    def process_item(self, item, spider):
        return item

class SankakuComplexImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{item["label"]}/{item["id"]}.jpg'

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        yield scrapy.Request(
            adapter['image_urls'],
            cookies={
                "login": 'spidiecrawler',
                "pass_hash": 'bea40334c081f54bacdac420e8391c11fe287668',
                "auto_page": '0'
            }
        )

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
