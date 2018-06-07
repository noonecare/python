"""
A 有 go  method 
B 继承 A, 重写 A 的 go 方法， 且调用 super().go
C 继承 B, 
"""


class A:
    def go(self):
        print("A")


class B(A):
    def go(self):
        super().go()
        print("B")


class C(B):
    def go(self):
        super().go()
        print("C")

# 无论如何， 继承中不应该出现环
# class D(B, C):
#     def go(self):
#         super().go()
#         print("D")


if __name__ == '__main__':
    c = C()
    c.go()

    # d = D()
    # d.go()
