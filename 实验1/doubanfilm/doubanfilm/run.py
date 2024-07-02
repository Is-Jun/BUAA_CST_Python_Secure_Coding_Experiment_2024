import time
import os
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from doubanfilm.spiders.douban import DoubanSpider


def run():
    if os.path.exists('douban_movies.csv'):  # 删除之前的CSV文件
        os.remove('douban_movies.csv')

    process = CrawlerProcess(get_project_settings())  # 创建爬虫进程
    process.crawl(DoubanSpider)
    process.start()
    print('爬取完毕，24小时后再次爬取')


if __name__ == '__main__':
    while True:
        run()
        time.sleep(24 * 60 * 60)  # 设置每24小时爬取一次
