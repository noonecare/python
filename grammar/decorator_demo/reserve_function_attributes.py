def decorate(func):
    """
    这是 decorate 函数的 docstring
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


@decorate
def add_one(a):
    return a + 1


@decorate
def original_function(a):
    """
    这是 original_function 的 docstring
    :param a:Int
    :return: Int
    """
    return a + 1


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
