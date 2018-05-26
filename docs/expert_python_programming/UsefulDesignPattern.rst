
python 已经非常灵活，有的设计模式没有必要（可以看成 Python 自带这些模式）。


Creation patterns
=================

相对于实现 Singleton, Python 更适合使用 Borg/MonoState 模式（就是让所有该类的对象，都有相同的状态）。Singleton 和 Borg 都可以使用
类的 **__new__** 方法实现。

在 Python 中，为什么 Borg 比 Singelton 常用？

要实现可以继承的 Singleton 比较麻烦（需要用到 metaclass）。而要实现可继承的 Borg 直接实现 **__new__** 即可，所以 Borg
用的比较多。

如果不用于继承，又要实现 Singelton, 直接使用模块级的变量和函数，即可。根本用不着实现 Singleton。这两个原因导致，Python
几乎用不着 Singleton。


Structural patterns
===================

Python 中如何定义接口?

可以使用 zope.interface 中的 Interface, implements 定义接口。虽然 zope 已经风光不再，但是 zope.interface 仍然常用。静态
语言能在编译时，警告你要实现 Interface 中的方法，Python 是动态语言，需要写测试用例，运行测试用例时，会提示你实现
Interface 中的方法。


使用 abc 包中的 abstractmethod 也可以定义接口。
重写 **__subhook__** 方法，可以定义 isinstance 行为。


Adapter
-------

可以认为 Python 自带了 Adapter, 因为 Python 采用了 Ducking Type 的模式，只要你有这个动作，就认为你是这个类。

所以我们要把 A 类配成 B 类，只要实现相应的方法就行，别的茶叶不用做（比如根本不用继承自 B 类）。


Ducking Type 的解释是： If you walks like a duck and talks like a duck, then it's a duck!




Proxy
-----

提供一个中间件，管控访问。比如之前的 url_cache。



Facade
------

在 **__init__.py** 中常见 import 语句，通过这些 import 语句，python 包定义了自己对外的接口。这就相当于是实现了 Facade 模式。




Behavioral patterns
===================


总体感觉平淡无奇。

Observer
--------


Visitor
-------

Template
--------

