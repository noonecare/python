# coding: utf-8
from unittest import TestCase

from crawler.scrapy_demo.BookCrawler import YunLaiGeCrawler


class TestYunLaiGeCrawler(TestCase):
    def test_get_book_url(self):
        test_chrome_driver_path = r"C:\Users\T440P\Downloads\chromedriver.exe"
        # 我欲封天 是 云来阁 小说网已经收录的一本小说，搜索 我欲封天 应该返回 我欲封天小说的 url
        assert (YunLaiGeCrawler.get_book_url("我欲封天", test_chrome_driver_path) == "http://www.yunlaige.com/html/6/6800/index.html")
        # 明朝那些事儿 是 云来阁 小说网没有收录的一本小说， 搜索 明朝那些事儿 应该返回 None
        assert (YunLaiGeCrawler.get_book_url("明朝那些事儿", test_chrome_driver_path) is None)

    def test_get_chapter_urls(self):
        test_book_menu_url = "http://www.yunlaige.com/html/6/6800/index.html"
        for chapter in YunLaiGeCrawler.get_chapter_urls(test_book_menu_url):
            print(chapter)

    def test_download(self):
        test_chapter_url = "http://www.yunlaige.com/html/6/6800/8931164.html"
        YunLaiGeCrawler.download(test_chapter_url)
