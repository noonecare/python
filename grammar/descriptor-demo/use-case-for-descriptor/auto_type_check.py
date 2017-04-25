# coding: utf-8
from decimal import Decimal, ROUND_UP
from tkinter import Widget

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
        try:
            return int(self.value)
        except:
            raise TypeError("Cannot be casted to int")

    def __set__(self, instance, value):
        try:
            self.value = int(value)
        except:
            raise TypeError("Cannot be casted to int")


class StringDescriptor(object):
    def __init__(self):
        self.value = None

    def __get__(self, instance, owner):
        try:
            return str(self.value)
        except:
            raise TypeError("Cannot be casted to int")

    def __set__(self, instance, value):
        try:
            self.value = str(value)
        except:
            raise TypeError("Cannot be casted to int")


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
    except TypeError:
        print("果然会发生 TypeError")
