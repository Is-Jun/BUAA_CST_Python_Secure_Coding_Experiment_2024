import scrapy
from buaa_cst.items import BuaaCstItem

class BuaaSpider(scrapy.Spider):
    name = 'buaa'
    allowed_domains = ['cst.buaa.edu.cn']
    start_urls = ['https://cst.buaa.edu.cn/']  # 导入页面

    def parse(self, response):
        # 取出新闻
        news = response.xpath('//ul[@class="dt-list2"]')

        # 取出标题和内容
        news_item = BuaaCstItem()
        news_item['title'] = news.xpath('.//div[@class="text"]/h3/text()').extract()
        news_item['content'] = news.xpath('.//div[@class="text"]/p/text()').extract()

        # 实例化
        yield news_item
