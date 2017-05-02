from unittest import TestCase


class Demo(TestCase):
    # unittest 太像 junit ，就连 method 的命名方式都和 junit 一模一样
    def setUp(self):
        print("先于所有 test method 执行")

    def tearDown(self):
        print("晚于所有 test method 执行")

    def testEqual(self):
        a = 3
        assert a == 1

    def testGreater(self):
        a = 4
        assert a > 4

    def testless(self):
        a = 4
        assert a < 4
