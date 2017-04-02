import types


# 写class decorator 时， __get__ 几乎一定是这个样子。所以今后写 class decorator 可以直接继承自 TemplateClassDecorator
# 这个类是我为了写 class decorator 写出来的语法糖
class TemplateClassDecorator:

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            # 为了展示 MethodType 我写了 MethodTypeShow 类
            return types.MethodType(self, instance)


# 简单演示如何使用 TemplateClassDecorator
class UseCaseDecorator(TemplateClassDecorator):
    def __init__(self, func):
        self.func = func
        print("use use case decorator initialized")

    def __call__(self, *args, **kwargs):
        print("use use case decorator")
        self.func(*args, **kwargs)


@UseCaseDecorator
def add(x, y):
    return x + y


class Spam:
    @UseCaseDecorator
    def bar(self, x):
        print(x)


if __name__ == '__main__':
    add(2, 3)
    spam = Spam()
    spam.bar(3)
