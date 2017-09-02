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
        pass
