class MyComplex:

    def __init__(self, r, i):
        self.real = r
        self.image = i

    def complex_add(self, other):
        self.real += other.real
        self.image += other.image

    def complex_minus(self, other):
        self.real = self.real - other.real
        self.image = self.image - other.image


# 只有当类的类名以 Test 开头的时候，nosetests 会把这个类识别为 test
# 其实严守 python 编码的规范， 并且记住以 test（函数用小写）/Test(类用大写) nosetests 就会识别为 test。
class TestMyComplex:

    data = MyComplex(1, 2)

    def test_complex_add(self):
        adder = MyComplex(2, 3)
        self.data.complex_add(adder)
        assert self.data.real == 3
        assert self.data.image == 5
        print("test complex add is correct.")
