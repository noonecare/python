"""
在 python 中， class 是继承于 type 的object
"""

a = type("DemoDynamicClass", (), {"greet": "Hello"})

print(a().greet)
print(a.__name__)

"""
用 decorator 自动添加作者信息
"""


def authenticate(x):
    return type(x.__name__, (), {"author": "wangmeng"})


@authenticate
class Demo:
    pass


print(Demo.author)


"""
对于类，常用的是 metaclass 这个在另一个文件中介绍
"""