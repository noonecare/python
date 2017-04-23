"""
用 __new__ 创建 instance
"""


class A:
    def go(self):
        print("A")

if __name__ == '__main__':
    a = object.__new__(A)
    a.go()

    b = A.__new__(A)
    b.go()
