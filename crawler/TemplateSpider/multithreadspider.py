import logging
from threading import Thread
from queue import Queue
import re
import requests
from bs4 import BeautifulSoup


class crawler(Thread):
    url_pattern = re.compile("{\"thumbURL\":\"([^\"]+)\"")

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            parameter = self.queue.get()
            # crawl 就是单线程的 爬虫，包括访问 url, 解析资源，保存资源。
            url = parameter
            response = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"})
            try:
                # 使用 BeautifulSoup 解析网页
                soup = BeautifulSoup(response.text, "lxml")
                # 找到网页中的第一个链接
                href = soup.select_one("a").get("href")
                print(href)
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

        urls = ["https://www.baidu.com"]
        # 向 queue 中填上数据，比如
        for item in urls:
            queue.put(item)

        queue.join()


if __name__ == '__main__':
    task = Task()
    task.start()
