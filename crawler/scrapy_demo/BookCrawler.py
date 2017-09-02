# coding: utf-8
import argparse
import logging
from queue import Queue
from threading import Thread

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class YunLaiGeCrawler(Thread):
    def __init__(self, queue):
        super(YunLaiGeCrawler, self).__init__()
        self.queue = queue

    def get_book_url(book_name, chrome_driver_path):
        browser = webdriver.Chrome(executable_path=chrome_driver_path)
        browser.get("http://www.yunlaige.com/")
        search = browser.find_element_by_id("searchkey")
        search.send_keys(book_name)
        submit = browser.find_element_by_name("submit")
        submit.click()
        book_url = browser.current_url
        if book_url != "http://www.yunlaige.com/modules/article/search.php":
            book_menu_url = browser.find_element_by_css_selector("a.readnow").get_attribute("href")
            return book_menu_url

    @staticmethod
    def get_chapter_urls(book_menu_url):
        soup = BeautifulSoup(requests.get(book_menu_url).text, "lxml")
        for chapter in soup.select("td > a"):
            yield book_menu_url[:-len("index.html")] + chapter.get("href")

    @staticmethod
    def download(chapter_url):
        soup = BeautifulSoup(requests.get(chapter_url).content.decode("GB18030"), "lxml")
        title = soup.select_one("title").text
        content = soup.select_one("div#content").text
        with open(title, "wt", encoding="utf-8") as f:
            f.write(content)

    def run(self):
        """
        主函数
        :return: 
        """
        while True:
            # 得到章节的 url
            chapter_url = self.queue.get()
            try:
                self.download(chapter_url)
            except Exception as e:
                # 如果出错，记录日志
                logging.error(str(e))
            finally:
                self.queue.task_done()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("book_name", type=str, help="请输入你想要爬取的小说名称")
    parser.add_argument("thread_num", type=int, help="请输入您希望的线程数")
    parser.add_argument("chrome_driver_path", type=str, help="请输入 chromedriver.exe 的路径")
    args = parser.parse_args()
    book_url = YunLaiGeCrawler.get_book_url(args.book_name, args.chrome_driver_path)

    if book_url is None:
        print("云来阁网站没有您要找的小说： {book_name}".format(book_name=args.book_name))
    else:

        queue = Queue()

        # 把要爬取章节的 url 放到 queue 中
        for chapter_url in YunLaiGeCrawler.get_chapter_urls(book_url):
            queue.put(chapter_url)

        for i in range(args.thread_num):
            t = YunLaiGeCrawler(queue)
            t.daemon = True
            t.start()

        queue.join()
        print("{book_name} 已经成功爬取".format(book_name=args.book_name))
