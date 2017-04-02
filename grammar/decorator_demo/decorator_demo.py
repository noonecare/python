from functools import wraps


def decorat(func):
    """
    这是 decorat 函数的 docstring
    :param func: A function 
    :return: another function
    """
    def h(*args, **kwargs):
        """
        这是构造出来的新函数的 docstring
        :param args: 
        :param kwargs: 
        :return: 
        """
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


@decorat
def original_function(a):
    """
    这是 original_function 的 docstring
    :param a:Int 
    :return: Int
    """
    return a + 1


# 这所以说bad 应为 h.__doc__ = func.__doc__ 必须在你执行一次被修饰的函数之后，才能生效。不执行被修饰的函数话，被修饰函数的
# docstring 还是 h 函数的 docstring
def bad_decorate_and_keep_docstring(func):
    """
    这是 decorate_and_keep_docstring 函数的 docstring
    :param func: 
    :return: 
    """
    def h(*args, **kwargs):
        """
        这是构造出来的函数的 docstring
        :param args:
        :param kwargs: 
        :return:
        """
        h.__doc__ = func.__doc__
        print("i am a decorator")
        return func(*args, **kwargs)
    return h


@bad_decorate_and_keep_docstring
def original_function1(a):
    """
    这是 original_function1 的 docstring
    :param a:Int 
    :return: Int
    """
    return a + 1


def good_decorate_and_keep_docstring(func):
    """
    这是 decorate_and_keep_docstring 函数的 docstring
    :param func: 
    :return: 
    """
    def h(*args, **kwargs):
        """
        这是构造出来的函数的 docstring
        :param args:
        :param kwargs: 
        :return:
        """
        print("i am a decorator")
        return func(*args, **kwargs)
    h.__doc__ = func.__doc__
    return h


@good_decorate_and_keep_docstring
def original_function2(a):
    """
    这是 original_function1 的 docstring
    :param a:Int 
    :return: Int
    """
    return a + 1


@good_decorate_and_keep_docstring
def original_function3(a: int):
    pass


def standard_decorate(func):
    # 加 wraps(func) 这一步是写 decorator 的好习惯，应当遵守这个惯例
    @wraps(func)
    def h(*args, **kwargs):
        """
        这是构造出来的新函数的 docstring
        :param args: 
        :param kwargs: 
        :return: 
        """
        print("i am a decorator")
        return func(*args, **kwargs)
    return h


@standard_decorate
def original_function4(a: int):
    """
    original_function4 的 docstring
    :param a: 
    :return: 
    """
    pass


if __name__ == '__main__':
    # print(add_one(3))
    # print(minus_one(3))
    # 用 decorat 修饰 original_function 之后， original_function 的 docstring 改变了
    print(original_function.__doc__)
    # 用 bad_decorate_and_keep_docstring 修饰 original_function1 之后， original_function1 的 docstring 改变了
    print(original_function1.__doc__)
    # 执行一次被修饰的 original_function1 函数， docstring 又变回来了
    original_function1(3)
    # docstring 又变回来了
    print(original_function1.__doc__)
    # 用 good_decorate_and_keep_docstring 修改时 original_function2 之后， original_function2 的 docstring 没有发生改变
    print(original_function2.__doc__)
    # 但是 function 的 attributes 不仅仅之后 docstring， 比如还有 annotations 。good_decorate_and_keep_docstring 没有能够
    # 保持不变 annotations。如果要保持 annotation 不变， python 标准库为此提供了 wraps 函数
    print(original_function3.__annotations__)
    # standard_decorate 修饰的函数，所有函数属性都不会变包括 docstring annotations 等等
    print(original_function4.__annotations__)
    print(original_function4.__doc__)
