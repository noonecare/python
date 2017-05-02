def fun(*args, **kwargs):
    for arg in args:
        print(arg)
    for kwarg in kwargs:
        print(kwarg)


if __name__ == '__main__':
    args = ["arg_{i}".format(i=i) for i in range(3)]
    kwargs = dict(zip(args, range(3)))

    fun(args, kwargs)
    fun(*args, **kwargs)

    fun("arg_0", "arg_1", "arg_2", name="wangmeng", birth=1989)
