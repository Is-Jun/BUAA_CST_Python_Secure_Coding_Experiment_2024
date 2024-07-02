import scrapy
from scrapy.exporters import CsvItemExporter


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        exporter = CsvItemExporter(open('douban_movies.csv', 'ab'), encoding='utf-8')  # 创建导入结果的csv文件
        exporter.start_exporting()
        for movie in response.xpath('//div[@class="info"]'):

            title = movie.xpath('div[@class="hd"]/a/span/text()').get()  # 电影标题
            director = movie.xpath('div[@class="bd"]/p/text()')[0].get().strip().split('\xa0\xa0')[0]  # 电影导演
            score = movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').get()  # 电影评分
            exporter.export_item({'title': title, 'director': director, 'score': score})

        exporter.finish_exporting()

        next_page = response.xpath('//span[@class="next"]/a/@href').get()  # 跳转下一页

        if next_page is not None:
            yield response.follow(next_page, self.parse)
