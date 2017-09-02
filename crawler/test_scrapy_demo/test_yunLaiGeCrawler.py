# coding: utf-8
from unittest import TestCase

from crawler.scrapy_demo.BookCrawler import YunLaiGeCrawler


class TestYunLaiGeCrawler(TestCase):

    def test_get_book_url(self):
        # 择天记是 云来阁 小说网已经收录的一本小说，搜索 择天记 应该返回 择天记小说的 url
        assert(YunLaiGeCrawler.get_book_url("我欲封天") == "http://www.yunlaige.com/book/6800.html")
        # 明朝那些事儿 是 云来阁 小说网没有收录的一本小说， 搜索 明朝那些事儿 应该返回 None
        assert(YunLaiGeCrawler.get_book_url("明朝那些事儿") is None)
