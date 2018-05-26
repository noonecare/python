from abc import abstractmethod, ABCMeta


class Pushable(metaclass=ABCMeta):
    @abstractmethod
    def push(self, x):
        pass


class PushStack(Pushable):
    def push(self, x):
        print("PushStack")
        print(x)


class P(Pushable):
    def show(self):
        pass


if __name__ == '__main__':
    p = PushStack()