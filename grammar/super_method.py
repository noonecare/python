# python2 和 python3  的 super 方法的使用是不同的， 本文件讲的都是 python3 中 super 函数的使用方法
# 菱形继承

class A:
    def go(self):
        print("A")


class B(A):
    def go(self):
        super().go()
        print("B")


class C(A):
    def go(self):
        super().go()
        print("C")


class D(B, C):
    def go(self):
        # B 和 C 之间没有基层关系，但是 mro 会把 method 的继承关系排成一条线，使得但就 go method, B 中的 go
        # 方法好像是继承之 C 一样。
        # 这是 python 继承中非常有个性的一点。
        super().go()
        print("D")


if __name__ == '__main__':
    d = D()
    d.go()


