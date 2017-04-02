import types


class MethodTypeShow:
    # define a attribute
    some_attr = "i am a string"
    a = "shit"


def f(x):
    print("i am f")
    print(x)

method_type_show = MethodTypeShow()
# 本来 f attribute 是个字符串类型
print(method_type_show.some_attr)
# 从 f 函数构造出 method。 构造的方式就是 result(*args, **kwargs) = f.__call__(method_type_show(这个参数一般记为
# instance), *args, **kwargs)
result = types.MethodType(f, method_type_show)
print(result)
# f 和 result 是不同的，类型也不同
print(id(f) == id(result))
print(type(f), type(result))
print(result)
# 把这个 method 绑定到 some_attr attribute
method_type_show.some_attr = result
# 执行这个 method
method_type_show.some_attr()



