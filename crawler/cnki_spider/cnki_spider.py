# coding: utf-8
import argparse
import random
from queue import Queue
from threading import Thread

import re
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
        :param journal: str 要查看那个期刊，比如“新文学史料”
        :param queue: Queue 从 queue 中取出目录页面的 url
        :param result_queue: Queue 把解析出来的文献的 url 放入到 result_queue 中
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

    def run(self):
        while True:
            catalog_url = self.queue.get()
            for resource_url in self.parseCatalogPage(catalog_url):
                self.result_queue.put(resource_url)
            self.queue.task_done()


class JournalUrlSpider(Thread):
    def __init__(self, journal):
        self.journal = journal

    @staticmethod
    def getJournalUrl(journal):
        search_url = r"http://navi.cnki.net/knavi/Common/Search/All"
        data = """{"StateID":"","Platfrom":"","QueryTime":"","Account":"knavi","ClientToken":"","Language":"","CNode":{"PCode":"SCDB","SMode":"","OperateT":""},"QNode":{"SelectT":"","Select_Fields":"","S_DBCodes":"","QGroup":[{"Key":"subject","Logic":1,"Items":[],"ChildItems":[{"Key":"txt","Logic":1,"Items":[{"Key":"txt_1","Title":"","Logic":1,"Name":"LY","Operate":"%","Value":"'新文学史料'","ExtendType":0,"ExtendValue":"","Value2":""}],"ChildItems":[]}]}],"OrderBy":"","GroupBy":"","Additon":""}}"""
        query_data = re.sub('"Value":"([^"]+)"', '"Value":"\'{journal}\'"'.format(journal=journal), data)

        response = requests.post(search_url,
                                 data={"SearchStateJson": query_data, "displaymode": 1, "pageindex": 1, "pagecount": 10,
                                       "index": 1, "random": random.uniform(0, 1)})
        soup = BeautifulSoup(response.text, "lxml")
        return "http://navi.cnki.net" + soup.select_one("dl.result h1 > a").get("href").strip()

    @staticmethod
    def _getStartYear(journal_url):
        response = requests.get(journal_url)
        soup = BeautifulSoup(response.text, 'lxml')
        for candidate in soup.select("p.hostUnit"):
            if "创刊时间" in candidate.text:
                return candidate.select_one("span").text

    @staticmethod
    def _getCatalogUrl(start_year, journal_url):
        pykm = re.search("baseid=([^&]+)", journal_url).group(1)
        template_url = "http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year={year}&issue={issue_num}&pykm={pykm}&pageIdx=0"

        for year in range(int(start_year), 2017):
            for issue_num in ["01", "02", "03", "04"]:
                yield template_url.format(year=year, issue_num=issue_num, pykm=pykm)

    def getCatalogUrl(self):
        journal_url = self.getJournalUrl(self.journal)
        start_year = self._getStartYear(journal_url)
        for url in self._getCatalogUrl(start_year, journal_url):
            yield url


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("journal_name", type=str, help="期刊的名字，注意是精确的名字")
    args = parser.parse_args()

    queue_1 = Queue()
    queue_2 = Queue()

    journalUrlSpider = JournalUrlSpider(args.journal_name)
    for catalog_url in journalUrlSpider.getCatalogUrl():
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
