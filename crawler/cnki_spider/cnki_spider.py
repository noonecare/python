# coding: utf-8
from queue import Queue
from threading import Thread

import requests
from bs4 import BeautifulSoup


class CnkiResourceSpider(Thread):
    """
    下载解析，摘要页面, 只要页面的 url 为
    """

    def __init__(self, queue):
        super(CnkiResourceSpider, self).__init__()
        self.queue = queue

    # 下载文献，解析文献
    def parseResource(self, resource_url: str):
        soup = BeautifulSoup(requests.get(resource_url).text, "lxml")
        title = soup.select_one("h2.title").text
        digest = soup.select_one("span#ChDivSummary").text
        journal = soup.select_one("p.title > a").text
        yield {"title": title, "digest": digest, "journal": journal}

    def run(self):
        while True:
            resource_url = self.queue.get()
            for item in self.parseResource(resource_url):
                print(item)
            self.queue.task_done()


class CnkiCatalogSpider(Thread):
    """
    从目录页面解析出所有摘要页面对应的 url, 目录页面的 url 为 http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=1978&issue=01&pykm=XWXS&pageIdx=0
    """

    def __init__(self, queue, result_queue):
        """
        :param queue: 从 queue 中取出目录页面的 url
        :param result_queue: 把解析出来的文献的 url 放入到 result_queue 中
        """
        super(CnkiCatalogSpider, self).__init__()
        self.queue = queue
        self.result_queue = result_queue

    @staticmethod
    def parseCatalogPage(catalog_url):
        """        
        :param catalog_url: 包含所有文章目录的页面 
        :return: 所有文章的 url
        """
        response = requests.get(catalog_url)
        soup = BeautifulSoup(response.text, 'lxml')
        for message in soup.select("a[onclick]"):
            yield message.get("onclick").split(",")[1].strip("'")

    @staticmethod
    def getCatalogUrl():
        # 这里以 新文学史料 为例
        template_url = "http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year={year}&issue={issue_num}&pykm=XWXS&pageIdx=0"

        for year in range(1978, 2017):
            for issue_num in ["01", "02", "03", "04"]:
                yield template_url.format(year=year, issue_num=issue_num)

    def run(self):
        while True:
            catalog_url = self.queue.get()
            for resource_url in self.parseCatalogPage(catalog_url):
                self.result_queue.put(resource_url)
            self.queue.task_done()


if __name__ == '__main__':
    queue_1 = Queue()
    queue_2 = Queue()

    for catalog_url in CnkiCatalogSpider.getCatalogUrl():
        queue_1.put(catalog_url)

    catalog_spider_num = 1
    for i in range(catalog_spider_num):
        t = CnkiCatalogSpider(queue=queue_1, result_queue=queue_2)
        t.daemon = True
        t.start()
    queue_1.join()

    resource_spider_num = 1
    for j in range(resource_spider_num):
        t = CnkiResourceSpider(queue=queue_2)
        t.daemon = True
        t.start()
    queue_2.join()
    print("所有内容已经成功爬取")
