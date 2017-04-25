# coding: utf-8
"""
python 有个弊端是， 变量不能绑定类型，在 debug 的时候，编译器能给我们的帮助有限。
对于 class attribute 用 descriptor 可以把变量绑定到特定类型的。

还有一些实际场景，一些数据需要检查，或者转换，或者对于访问权限有控制。这些都可以用
descriptor 来实现。我举个累着，如果用 现金交易， 只能精确到分，你可以写个 
descriptor 自动把 float 截取到小数点后两位。
"""


class IntDescriptor(object):
    def __init__(self):
        self.value = None

    def __get__(self, instance, owner):
        return int(self.value)

    def __set__(self, instance, value):
        self.value = int(value)
        if self.value < 0 or self.value > 200:
            raise ValueError("一个人不可能活这么长")


class StringDescriptor(object):
    def __init__(self):
        self.value = None

    def __get__(self, instance, owner):
        return str(self.value)

    def __set__(self, instance, value):
        self.value = str(value)


class TypedAttribute:
    age = IntDescriptor()
    name = StringDescriptor()

    def __init__(self, name, age):
        self.name = name
        self.age = age


if __name__ == '__main__':
    a = TypedAttribute("1", "3")
    print(a.age)
    print(type(a.age))
    print(a.name)

    try:
        b = TypedAttribute(3, "不能转成int")
    except ValueError:
        print("果然发生了异常")

    try:
        c = TypedAttribute("zhangsanfeng", 300)
    except ValueError as e:
        print(str(e))
