==========================
Subclassing built-in types
==========================


built-in types 当然可以 Subclassing, 没有什么大不了的。需要注意的是， built-in types 支持些特别的运算符。只要重写 built-in
type 的某些方法，就可以重定义这些运算符。

这些运算符和方法如下

+----------+-------------+
| Operator | method      |
+==========+=============+
| a[k]=1   | __setitem__ |
+----------+-------------+
| a[k]     | __getitem__ |
+----------+-------------+
| ==       | __eq__      |
+----------+-------------+

>,<,==,<>,<=,>= 最好使用 `totalordering` decorator 来定义， 不要只自定义 \_\_le\_\_, \_\_gl\_\_ 方法。
in 最好继承 list， set, dict 去实现，不要只自定义 \_\_contains\_\_ 方法。
+， -， *，/, // 这些运算符也可以重写。


在重写运算符，继承 built-in types 时，应该先去 collections 包中找找有没有现成的实现。大多数情况写，用不着重写运算符，继承
built-in types 的。


Access methods from superclass
------------------------------


super() 用于 Access methods from superclass。
super() 可以用在任何上下文中，不一定非要在类方法中出现。
super() 常见的用法有如下三种：

    super(instance_type, instance_value): instance_value 必须属于 instance_type 否则会报错。instance_value 属于
    instance_type 的情况下，返回 instance_value 对应的 type 的 mro 中 instance_type 后一个 class。

    super(instance_type): 返回 instance_type 的 mro 中 instance_type 后一个 class。

    super(): python3 的语法（Python2 不支持），出现在类方法中。如果 super() 出现在普通方法中，相当于 super(defined_class,
    self)；如果出现在普通的类方法中相当于 super(defined_class)；如果出现在 staticmethod 中会报 RuntimeError。


除了使用 super() Access methods from superclass，还可以使用 superclass 的类名直接访问 superclass 的方法。尽量不要同时使用
super 和 superclass 类名两种访问 methods from superclass 的方法。

Python 子类默认不会调用父类的 `__init__` 函数（初始化函数），如果需要，需要开发者自行调用，调用时，如果不清楚父类 `__init__`
函数的 signature, 可以查文档或者读源码，使用 IDE 的话，这很容易。

Python3 所有的类都继承自 `object` 类， Python2 中有继承自  `object` 的类，也有不是继承自 `object` 的类。继承自 `object` 的类
称为新式类(new style class)，不是继承自 `object` 的类称为旧式类(old style class)。新式类使用 C3 算法解决多重继承问题，旧式类
使用深度优先解决多重继承问题。新式类有 `mro` 方法和 `__mro__` 属性；旧式类没有。

Python3 中所有类都是新式类，不管怎么定义类。 Python2 中只有明确继承自 object 或者继承自其它新式类的类都是新式类。除此之外是旧
式类。比如如下 Python2 代码：

.. code-block::

    # 旧式类
    class A:
        pass

    # 旧式类
    class B():
        pass

    # 旧式类
    class C(A):
        pass

    # 新式类
    class D(object):
        pass

    # 新式类
    class E(D):
        pass


如果代码要运行在 Python2 和 Python3 环境，那么定义类时，一定要指明继承于那个类。一定都用新式类。

即使旧式类没有 mro ，但是仍然可以使用 `super` 。最好不要用旧式类。

mro(method resolve order)， Python 新式类使用 C3 算法计算 mro。对于多重继承，C3 给出给类的线性排列。C3 算法计算公式为：

.. code-block::

    class MyClass(Base1, Base2):
        pass

L(MyClass) = MyClass + merge(L[Base1], L[Base2], Base1, Base2)


merge:

    list head 表示list 的第一个元素，list 的 tail 表示 list 中除了第一个元素外的其他元素。

    good head, 如果一个 list 的 head, 不出现在任何一个其他 list 的 tail 中。那么这个 head 称为 good head。

    从做到右，寻找 good head， 如果找到 good head，把 good head 添加到 MyClass 的 MRO 中，并且把 good head 从其他merge 的
    list 中删除。继续寻找 good head，知道所有 list 为空，那么 MRO 构造完成；或者 list 不为空，但是找不到 good head,无法创建
    类，报错。


我说的不仔细，还是用原话说吧：

    .. code-block::

        The linearization of C is the sum of C plus the merge of the linearizations of the parents and the list of the
        parents.

        Taken the head of the first list, that is, L[Base1][0]; if this head is not in the tail of any of the other
        lists, then add it to the linearization of MyClass and remove it from the lists in the merge, otherwise look at
        the head of the next list and take it, if it is a good head.

        Then, repeat the operation until all the classes are removed or it is impossible to find good heads. In this
        case, it is impossible to construct the merge, Python 2.3 will refuse to create the class MyClass and will raise
        an exception.




super pitfall
-------------

Mixing super and explicit class calls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



Heterogeneous arguments
^^^^^^^^^^^^^^^^^^^^^^^

不清楚父类 `__init__` 方法的 signature。我不认为这是什么问题，有 IDE 的帮助，很容易知道父类 `__init__` 方法的 signature。



Best Practices
^^^^^^^^^^^^^^

#. 尽量不要使用多重继承
#. super 和 explicit class calls 不要混在一起使用
#. 定义类时继承自 Object 如果你的代码要兼容 Python2
#. 调用父类方法时，确认下父类是谁（比如用 mro() 方法）


Advanced attribute access pattern
=================================

name mangling, 《Expert Python Programming》 反对使用 name mangling, 认为使用 _ 足够了。

Descriptor
----------


Descriptor are the base of a complex attribute access in Python.


descriptor protocol:

#. `__set__(self, obj, type=None)`
#. `__get__(self, obj, value)`
#. `__delete__(self, obj)`

A descriptor that implements `__get__()` and `__set__()` is called ***data descriptor**.  If it just implements
`__get__()`, then it is called a **non-data descriptor**.


不管是 `instance.attribute` 或者是 `getattr(instance, 'attribute')`, 都是调用 `__getattribute__()` 去寻找属性，
`__getattribute__()` 寻找属性的默认顺序为：

#. It verifies if the attribute is a data descriptor on the class object of the instance.
#. If not, it looks to see if the attribute can be found in the `__dict__` of the instance object.
#. Finally, it looks to see if the attribute is a non-data descriptor on the class object of the instance.

我认为这段描述没有谈到 MRO 对于 `__getattribute__()` 的影响。

Real-life example - lazily evaluated attributes
-----------------------------------------------





