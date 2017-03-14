b = 1


def h(a=b):
    return a

print("parameter a's default value is {default_value}".format(default_value=h()))

b = 2

print("even though b changed its value, parameter a's default value didn't change. a's "
      "default value is still {default_value}".format(default_value=h()))
