def decorat(func):
    def h(*args, **kwargs):
        print("i am a decorator")
        return func(*args, **kwargs)
    return h


@decorat
def add_one(a):
    return a + 1
#  上面的decorator 其实是执行了 add_one = decorate(add_one)


# 实现带参数的 decorator
def decorate_use_parameter(greeting: str):

    def decorator(func):
        def h(*args, **kwargs):
            print(greeting)
            return func(*args, **kwargs)
        return h
    return decorator


@decorate_use_parameter("Hello")
def minus_one(a):
    return a - 1


if __name__ == '__main__':
    print(add_one(3))
    print(minus_one(3))
