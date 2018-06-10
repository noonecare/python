"""
    patch 要比 Mock 简单，常用
    但是 patch 是通过调用 Mock 实现的
    所以对于 Mock ， 心中应该有个概念

    Mock 是一个可以伪装成任何类的类
    对于 Mock 类, 你可以任意指定它的 attribute。
    特别的，指定 spec 参数（值为一个类），就会为 Mock 类赋予该类所有的 attribute。
    这样从外部看（这个类的使用者），这个 Mock 和 spec 值表示的类是完全相同的。当然从内部看 Mock 类的行为一般要比 spec 指明的类简单的多。
"""

from cmath import sqrt
from unittest.mock import Mock


# 表示一个复数
class Complex:
    def __init__(self, x, y):
        self.real = x
        self.image = y

    def complex_add(self, other):
        self.real += other.real
        self.image += other.image

    def complex_minus(self, other):
        self.real -= other.real
        self.image -= other.image

    def complex_multiply(self, other):
        self.real = self.real * other.real - self.image * other.image
        self.image = self.real * other.image + self.image * other.real

    # 求出共轭的复数
    def complex_company(self):
        return Complex(self.real, -self.image)

    # 求出模
    def complex_length(self):
        return sqrt(self.real * self.real + self.image * self.image)

    def __eq__(self, other):
        return other.real == self.real and other.image == self.image

    # 除以标量
    def divide_scalar(self, scalar):
        self.real = self.real / scalar
        self.image = self.image / scalar
        return self


a = Mock(spec=Complex)
# a 已经有了 complex_add 和 complex_minus 方法
'complex_add' in dir(a)
'complex_minus' in dir(a)

# a.complex_add 也是个 Mock, a.complex_add 的 return_value 和 side_effect 都为 None
a.complex_add(Complex(0, 0))


# 求 1 / r
def calculate_inverse(x: Complex):
    if x == Complex(0, 0):
        return Complex(0, 0)
    else:
        return x.complex_company().divide_scalar(x.complex_length() * x.complex_length())


# 验证上面的函数是否正确时，我们会用几个实际的复数去测试，比如用 0+0 * i, 1, i
def test_calculate_f():
    fake_complex = Mock(spec=Complex)
    fake_complex.side_effect = [Complex(0, 0), Complex(1, 0), Complex(0, 1)]
    # 这几个复数的共轭
    fake_complex.complex_company = [Complex(0, 0), Complex(1, 0), Complex(0, -1)]
    # 这几个复数的模
    fake_complex.complex_length = [0, 1, 1]
    expected_inverse = [Complex(0, 0), Complex(1, 0), Complex(0, -1)]
    for i in range(len(expected_inverse)):
        assert calculate_inverse(fake_complex()) == expected_inverse[i]

# 上面的例子演示了最常用的例子，就是用具体几个点的值，验证全局的正确性
# 想象这样一个场景，你和你的开发伙伴（记为 A）分别开发两个 module, 其中你的 module 要引用 A 开发的 module（记为 P）。
# 你和 A 提前约定了好了接口，所以你不用等 A 开发完，你就已经知道了 P 的外部行为，知道了对于一些特定的输出，P 应该返回的结果。
# 这样你直接可以 mock 一个 P（对于指定的输入返回指定的输出）, 用于测试你的代码（不用等 A 写好了 P 再测试）。
