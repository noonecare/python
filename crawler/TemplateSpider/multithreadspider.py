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
            url = "https://www.amazon.cn/s/ref=nb_sb_noss_1?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&field-keywords={search_word}".format(search_word=parameter)

            url = "https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/dp/B00XJ8LGWG/ref=sr_1_1?ie=UTF8&qid=1487734705&sr=8-1&keywords=%E8%92%99%E6%9B%BC"
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"})
            try:
                print(response.text)
                soup = BeautifulSoup(response.text, 'lxml')
                keyword = parameter
                categroy_1 = soup.select_one("#SalesRank > ul > li > span.zg_hrsr_ladder > a").text
                categroy_2 = soup.select_one("#SalesRank > ul > li > span.zg_hrsr_ladder > a + a").text
                categroy_3 = soup.select_one("#SalesRank > ul > li > span.zg_hrsr_ladder > a + a + a").text
                print(keyword, categroy_1, categroy_2, categroy_3)
            except Exception as e:
                logging.error()
                logging.error(str(e))

            self.queue.task_done()


class Task(object):
    def start(self):
        queue = Queue()
        for i in range(100):
            t = crawler(queue)
            t.daemon = True
            t.start()

        urls = ["蒙曼"]
        # 向 queue 中填上数据，比如
        for item in urls:
            queue.put(item)

        queue.join()


if __name__ == '__main__':
    task = Task()
    task.start()
