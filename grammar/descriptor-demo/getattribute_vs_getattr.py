# coding: utf-8


# attribute access
class MyDescriptor(object):
    def __get__(self, instance, owner):
        print("descriptor")


class Demo:

    a = MyDescriptor()

    def __getattr__(self, item):
        print("getattr is running")


class PrintErrorMsgButNoException:
    """
    这个例子，通过实现 __getattr__
    使得，当你访问不存在的 attribute 时，不会产生异常，只是打印出 no {item} found
    """
    a = 1

    def __getattr__(self, item):
        print("no {item} found".format(item=item))

if __name__ == '__main__':
    t = PrintErrorMsgButNoException()
    # 本来应该报错的，但是因为我刚才定义了 __getattr__ 所以不会报错
    t.b
    # 直接调用 __getattribute__ 还是会报错
    try:
        t.__getattribute__("b")
    except AttributeError:
        print("如果直接执行 __gettribute__ 还是会报 AttributeError 错误")

    demo = Demo()
    demo.a
    demo.b
