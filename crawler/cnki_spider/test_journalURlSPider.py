# coding: utf-8
from unittest import TestCase

from crawler.cnki_spider.cnki_spider import JournalUrlSpider


class TestJournalURlSPider(TestCase):
    def testParse(self):
        assert (JournalUrlSpider.getJournalUrl(
            "新文学史料") == "http://navi.cnki.net/KNavi/pubDetail?pubtype=journal&pcode=CJFD&baseid=XWXS")

    def testStartYear(self):
        assert (JournalUrlSpider._getStartYear(JournalUrlSpider.getJournalUrl("新文学史料")) == "1978")

    def testGetCatalogUrl(self):
        for url in JournalUrlSpider._getCatalogUrl("1978", JournalUrlSpider.getJournalUrl("新文学史料")):
            print(url)
