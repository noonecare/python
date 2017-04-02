# decorator 还可以写成 class 的形式
import types


class Profiled:
    a = 1

    def __init__(self, func):
        self.func = func
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.func(*args, **kwargs)

    # 为了能够使 Profiled 类既能装饰 function, 也能装饰 method
    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            # 为了展示 MethodType 我写了 MethodTypeShow 类
            return types.MethodType(self, instance)


@Profiled
def add(x, y):
    return x + y

# 定义时，执行了 add = Profile(add)


class Spam:
    @Profiled
    def bar(self, x):
        print(x)


if __name__ == '__main__':
    # print(add(2, 3))
    # print(add.ncalls)
    spam = Spam()
    # spam.bar， 实际是在执行 bar.__get__(spam, Spam)， spam 参数不为 None, 所以 spam.bar 是 types.MethodType(self,
    # instance)
    # types.MethodType(self, instance) 的结果是个定义了 __call__ 方法的类，同时是个 method， 这个 method （我记为 result）
    # 的 __call__ 由原来定义的 profile.__call__ 转变而来。 具体来说现在这个 method 执行 call, result.__call__(*args, **
    # kwargs) 等价于 bar.__call__(self, *args, **kwargs)。result 其他的 attribute 和 bar 的 attributes 都一样
    print(spam.bar)
    print(spam.bar(3))
    print(spam.bar.a)
