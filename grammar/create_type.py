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
    item = {'author': 'wangmeng'}
    for attr in dir(x):
        item[attr] = getattr(x, attr)

    return type(x.__name__, (), item)
    # return type(x.__name__, (), {})


@authenticate
class Demo:
    def greet(self):
        print("Hello")


print(Demo.author)
Demo().greet()
"""
对于类，常用的是 metaclass 这个在另一个文件中介绍
"""