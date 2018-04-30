from abc import ABCMeta, abstractmethod


class Pushable(metaclass=ABCMeta):

    @abstractmethod
    def push(self, x):
        """"""




    @classmethod
    def __subclasshook__(cls, C):
        if cls is Pushable:
            if any("push" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


class SomethingWithPush:
    def push(self, x):
        pass


print(isinstance(SomethingWithPush(), Pushable))

class A(object):
    def hello(self):
        pass




print(isinstance(A(), Pushable))