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


def test_f_use_decorator():
    # patch 也常常写成 decorator, patch decoder 会把 mock 出来的对象(属于 Mock 类， 这一点和 上面用 context manager 方式调
    # 用 patch 不同， 用 context manager 的方式调用 patch, patch 出来的对象时 new 指定的类型)赋予 所修饰的函数的最后一个参数
    # patch 的第一个参数应当是 package.module.classname
    @patch("sys.stdout", new_callable=StringIO)
    def f_use_decorator(fake_out):
        f()
        assert fake_out.getvalue() == "success\n"

    f_use_decorator()


if __name__ == '__main__':
    test_f_use_decorator()
