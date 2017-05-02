# coding: utf-8


class Singleton(type):
    """
    实现 Singleton Pattern, 这是从 《Python Cookbook3》 中抄的代码
    """
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)
        print("Creating Singleton")

    def __call__(self, *args, **kwargs):
        """
        __call__ 的默认行为是依次执行 Singleton.__new__ Spam.__init__;
        这里重写了 __call__ 使得 Spam 类初始化时（执行 s = Spam() 语句时），不再依次执行 __new__ 和 __init__ 而是采用了
        自定义的行为 
        """
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


# 指定 metaclass=Singleton 时，默认会执行 Singleton.__init__() 的
class Spam(metaclass=Singleton):
    def __init__(self):
        print("Creating Spam")

# 我画这条分割线，就是为了证明， Singleton 的 __call__ 默认是调用 Singleton.__new__; Spam.__init__; 当然这里 Singleton
# override 了 __call__ method, 所以行为不同了
print("++++++++++++++++++++++++++++")

if __name__ == '__main__':
    # Spam() 会调用 Singleton.__call__
    s_1 = Spam()
    # 为什么不再打印 Creating Spam
    s_2 = Spam()
    s_3 = Spam()
