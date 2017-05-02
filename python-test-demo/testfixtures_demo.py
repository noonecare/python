"""
演示 tempfile 和 str_today_1
"""

import tempfile

from testfixtures import Replace, test_date
from testfixtures.tests.sample1 import str_today_1


# 写个简单的例子，向文件中写入今天的日期
def diary(today, fp):
    # 写入日期
    fp.write(today + "\n")


def test_diary():
    with tempfile.TemporaryFile('w+t', encoding="utf-8") as f:
        with Replace('testfixtures.tests.sample1.date', test_date(1978, 6, 13)):
            diary(str_today_1(), f)
            diary(str_today_1(), f)
            f.seek(0)
            assert f.read() == "1978-06-13\n1978-06-14\n"
