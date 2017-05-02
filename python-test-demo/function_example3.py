# 不管是开头含有 test, 还是结尾含有 test nosetests 都会把这个 function/method/class 等等认为是 test 去执行
# 但是如果开头没有 test, 结尾也没有 test 那么 nosetests 就不认为是 test.


def lesser():
    a = 4
    assert a < 4
