import scrapy
from scrapy.loader import ItemLoader
from sankaku_complex.items import SankakuComplexItem
import sankaku_complex.secret as secret

class SankakuComplexSpider(scrapy.Spider):
    name = 'sankaku-complex'
    allowed_domains = ['chan.sankakucomplex.com']

    def __init__(self, tags="", name=None, passwd=None):
        super(SankakuComplexSpider, self).__init__()
        if tags != "":
            tags = 'tags=' + tags
        self.tags = tags

    def start_requests(self):
        yield scrapy.FormRequest(
            'https://chan.sankakucomplex.com/user/login',
            formdata={'url': '', 'user[name]': secret.USER_NAME, 'user[password]': secret.USER_PASSWORD, 'commit': 'Login'},
            callback=self.logged_in
        )

    def logged_in(self, response):
        yield scrapy.Request(
            f'https://chan.sankakucomplex.com/?page=1&{self.tags}+order:random',
            cookies={
                "login": 'spidiecrawler',
                "pass_hash": secret.USER_PASSWORD_HASH,
                "auto_page": '0'
            },
            callback=self.parse
        )

    def parse(self, response):
        posts = response.xpath('//span[@class="thumb blacklisted"]/a')

        for post in posts:
            item = SankakuComplexItem()
            item['id'] = post.xpath('@href').get().split('/')[-1]
            item['title'] = post.xpath('img/@title').get()
            item['image_urls'] = 'https://chan.sankakucomplex.com' + post.xpath('img/@src').get().split('sankakucomplex.com')[-1]
            if '-tomboy+1girl+-male+-futanari' in self.tags:
                item['label'] = 'girl'
            elif '-trap+1boy+-female+-futanari' in self.tags:
                item['label'] = 'boy'
            elif 'tomboy+1girl+-male+-futanari' in self.tags:
                item['label'] = 'tomboy'
            elif 'trap+1boy+-female+-futanari' in self.tags:
                item['label'] = 'trap'
            else:
                item['label'] = 'other'
            yield item
