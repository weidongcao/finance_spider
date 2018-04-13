from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {

    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://scrapy.org/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"').items():
            self.crawl(each.attr.href, callback=self.detal_page)

    def detail_page(self, response):
        return {
            "url": response.url,
            "titlt": response.doc('title').text()
        }
