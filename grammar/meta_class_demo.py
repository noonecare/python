
def authenticate(future_class_name, future_class_parents, future_class_attr):
    future_class_attr.update({'author': 'wangmeng'})
    return type(future_class_name, future_class_parents, future_class_attr)


class AuthenticateClass(type):

    def __new__(cls, future_class_name, future_class_parents, future_class_attr):
        future_class_attr.update({'author': 'wangmeng'})
        return type(future_class_name, future_class_parents, future_class_attr)


# 创建类时，默认的 metaclass 是 type, 传给type 的三个参数是 future_class_name, future_class_parents, future_class_attr，
# type 返回的是个 type 类型的 instance(其实就是 class)
class Demo(metaclass=AuthenticateClass):
    def greet(self):
        print("Hello")


Demo().greet()
print(Demo.author)
