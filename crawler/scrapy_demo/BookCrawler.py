# coding: utf-8
from urllib.parse import quote

import requests
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver

chrome_driver_path = r"C:\Users\T440P\Downloads\chromedriver.exe"


class YunLaiGeCrawler:
    def get_book_url(book_name):
        browser = webdriver.Chrome(executable_path=chrome_driver_path)
        browser.get("http://www.yunlaige.com/")
        search = browser.find_element_by_id("searchkey")
        search.send_keys(book_name)
        submit = browser.find_element_by_name("submit")
        submit.click()
        book_url = browser.current_url
        if book_url != "http://www.yunlaige.com/modules/article/search.php":
            return book_url

    def get_book_menu(self, book_url):
        """
        由书的连接得到所有章节，以及所有章节的链接
        :return: 所有章节的链接
        """
        pass

    def download(self, chapter_url):
        """
        有章节的 url 下载章节的内容
        :param chapter_url: 章节对应的url
        """

    def run(self):
        """
        主函数
        :return: 
        """
        pass
