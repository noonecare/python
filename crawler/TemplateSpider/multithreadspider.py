import logging
from threading import Thread
from queue import Queue
import re
import requests
from bs4 import BeautifulSoup


class crawler(Thread):
    """
    爬虫模板，自定义爬虫时，需要自己重写 make_request， parse, saveItem 方法。
    """

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    @staticmethod
    def make_request(param):
        """
        从 param 中构造要发送的 request
        :param param: 从 self.queue 中取出的参数
        :return: 构造出的 request 或者 url
        """
        return "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd={query}".format(query=param)

    @staticmethod
    def parse(text):
        """
        解析页面的逻辑，从网页得到结果话的数据（比如返回一个 dict）的列表, 如果在解析的过程中需要发送新的 request 请把 reqeust 添加到 self.queue 中
        :param text: 
        :return: 
        """
        # 使用 BeautifulSoup 解析网页
        # 这里把百度返回结果的 title 解析出来
        soup = BeautifulSoup(text, "lxml")
        return [item.text for item in soup.select("div.result.c-container a")]

    @staticmethod
    def saveItem(item):
        """
        把解析后的结果保存起来，比如保存到文件中
        :param item: 解析页面得到的结果
        """
        # 这里简单地把结果打印到控制台，更常见的操作是保存成文件，或者保存到数据库中
        print(item)

    def run(self):
        while True:
            parameter = self.queue.get()
            # crawl 就是单线程的 爬虫，包括访问 url, 解析资源，保存资源。
            url = self.make_request(parameter)
            text = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}).text
            try:
                for item in self.parse(text):
                    self.saveItem(item)
            except Exception as e:

                logging.error(str(e))

            self.queue.task_done()


class Task(object):
    def start(self):
        queue = Queue()
        for i in range(100):
            t = crawler(queue)
            t.daemon = True
            t.start()

        params = ["python", "scala", "cmake"]
        # 向 queue 中填上数据，比如
        for item in params:
            queue.put(item)

        queue.join()


if __name__ == '__main__':
    task = Task()
    task.start()
