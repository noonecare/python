#  测试的时候可能需要一些假的组件。比如函数正确工作之后，应当打印出 success。 你想检验函数是否真的输出了 success。这时候，
# 你需要 mock stdout。
from io import StringIO
from unittest.mock import patch


def f():
    # do some work
    print("success")


def test_f():
    # 把 sys.stdout 导成 StringIO()
    with patch(target="sys.stdout", new=StringIO()) as fake_out:
        f()
        assert fake_out.getvalue() == 'success\n'
