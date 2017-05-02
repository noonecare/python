# coding: utf-8

"""
val = MyDescriptor()
中把 MyDescriptor() 绑定在了 val 变量，但是 MyDescriptor() 不知道自己的变量名叫 val。
本实例说明这个问题。
"""


class ManualDescriptor(object):
    def __init__(self, field=""):
        self.field = field

    def __get__(self, instance, owner):
        print("Called __get__")
        return instance.__dict__.get(self.field)

    def __set__(self, instance, value):
        print("Called __set__")
        instance.__dict__[self.field] = value


class ManualDescriptorDemo:

    # 手动写出变量名，这当然可以，不过手动不如自动
    val = ManualDescriptor("val")


# 用 decorator 搞到变量名
def named_descriptor(klass):
    for name, attr in klass.__dict__.items():
        if isinstance(attr, ManualDescriptor):
            attr.field = name
    return klass


# 手动改自动
@named_descriptor
class AutoDemo(object):
    x = ManualDescriptor()

if __name__ == '__main__':
    demo = ManualDescriptorDemo()

    demo.val = 4
    print(demo.val)

    auto_demo = AutoDemo()
    auto_demo.x = 3
    print(auto_demo.x)
