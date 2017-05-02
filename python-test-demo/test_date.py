from io import StringIO
# python2.7 没有 unittest.mock，代码只对 python3 是可执行的
from unittest.mock import Mock, patch

from testfixtures import Replace, test_date
from testfixtures.tests.sample1 import str_today_1


def demonstrate_today():
    print(date.today())


@patch("sys.stdout", new_callable=StringIO)
def test_demonstrate_today(fake_out):
    with Replace('testfixtures.tests.sample1.date', test_date(1978, 6, 13)):
        global date
        date = Mock()
        date.today = str_today_1
        demonstrate_today()
        assert fake_out.getvalue() == "1978-06-13\n"


if __name__ == '__main__':
    demonstrate_today()
