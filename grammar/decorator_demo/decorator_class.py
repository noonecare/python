# decorator 还可以写成 class 的形式
class Profiled:
    def __init__(self, func):
        self.func = func
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.func(*args, **kwargs)


@Profiled
def add(x, y):
    return x + y

# 定义时，执行了 add = Profile(add)


if __name__ == '__main__':
    print(add(2, 3))
    print(add.ncalls)
    print(add(2, 3))
    print(add.ncalls)
    print(add(2, 3))
    print(add.ncalls)
    print(add(2, 3))
    print(add.ncalls)
    print(add(2, 3))
    print(add.ncalls)
