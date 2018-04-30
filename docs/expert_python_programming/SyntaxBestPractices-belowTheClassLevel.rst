Python's built-in types
=======================

Strings and bytes
-----------------

Python2 和 Python3 在表示字符串时有很大不同。

在 Python2 中，有 bytes, unicode, str 和 basestring 类型。 bytes == str, unicode != str, bytes 和 unicode 都继承于
basestring 。

    .. code-block::

        >>> type(u"hello world")
        <type 'unicode'>
        >>> type(b"hello world")
        <type 'str'>
        >>> isinstance(u"hello world", str)
        False
        >>> isinstance(u"hello world", basestring)
        True
        >>> bytes
        <type 'str'>
        >>> isinstance(b"hello world", str)
        True
        >>> isinstance(b"hello world", basestring)
        True

在 Python3 中，有 bytes, str 类型，没有 unicode, basestring 类型。bytes != str。所有 str 都是用 unicode 编码的字符串。b 字
符串前缀表示是 bytes literal， u 字符串前缀已经没有语法含义，但是为了和 Python2 后向兼容，也可能会写上。Python2 源码文件的默认
编码是 ASCII, Python3 源码文件的默认编码是 UTF-8。如果不用考虑 Python2 和 Python 3 的兼容性，那么声明默认编码显得多此一举；如
果代码要考虑 Python2 和 Python3 的兼容性。


Python3 bytes 是 immutable 的， bytearray 是 mutable 的。

得到 bytes

    #. bytes(source, encoding, errors)
    #. str.encode(encoding, errors)

得到 str

    #. str(source, encoding, errors)
    #. bytes.decode(encoding, errors)

errors 是处理编码解码错误的机制，可选的 options 有： replace, ignore, strict, xmlcharrefreplace, 或者其他注册过的 handler，
查看 codecs 模块文档。


Implementation details
^^^^^^^^^^^^^^^^^^^^^^

str 和 bytes 是 immutable 的，所以也是 hashable 的。一般 mutable 的数据，不会整成 hashable 的（在 Python 中应该没有 mutable
的数据是 hashable 的）。


String Concatenation
^^^^^^^^^^^^^^^^^^^^

join 效率几乎总是比字符串相加要高（有特列，但很少，可忽略）。如果能用 format 尽量用 format 和 %，因为可读性好。



Collections
-----------

#. List
#. Tuple
#. Dictionaries
#. Sets


List and tuples
^^^^^^^^^^^^^^^

tuple is **immutable** and **hashable**.

与我想的不同，List 并不是用链表实现的。而是用连续一段内存表示的。具体来说：就是 List 保存着List 实际长度，和连续内存长度。
如果List 的实际长度超过分配的内存长度，那么会重新分配内存，比如分配 2x内存长度 的内存。如果List 的实际长度小于分配长度的 1/2。
就会收回1/2 内存长度的内存。这样使得：

append 操作的摊余成本是 O(1), 但是某一次的时间复杂度可能是 O(n), n 是 List 的长度。


List comprehensions
^^^^^^^^^^^^^^^^^^^

.. code-block::

    [i for i in range(10) if i % 2 == 0]


.. code-block::

    for i, element in enumerate(['one', 'two', 'three']):
        print(i, element)


    for item in zip([1, 2, 3], [4, 5, 6]):
        print(item)

    for item in zip(*zip([1, 2, 3], [4, 5, 6])):
        print(item)

    # unpack
    first, second, third = "foo", "bar", 100
    first, second, *rest = 0, 1, 2, 3
    first, *inner, last = 0, 1, 2, 3
    (a, b), (c, d) = (1, 2), (3, 4)


Dictionaries
------------


.. code-block::

    squares = {number: number**2 for number in range(100)}



Python2 中 dictionaries 的 keys(), values() 和 items() 返回的是当前 dictionaries 的 keys, values 和 items。
Python3 中 dictionaries 的 keys(), values() 和 items() 返回的是 dictionaries 的 keys 的view, values 的 view 和 items 的
value。可以认为是执行 dictionaries 的 keys, values 和 items 的指针。这样的好处是: 比如 a = dict_item.keys() 之后 dict_item
添加了很多 key, 此时 a 中包含了新添加的 keys；而 Python2 中是不包含的。下面这段代码，Python2 和 Python3 的执行结果是不同的。

.. code-block::

    >>> words = {'foo': 'bar', 'fizz': 'bazz'}
    >>> items = words.items()
    >>> words["spam"] = 'egg'
    >>> items


最后， Python3 中 keys() 中key 出现的顺序刚好和 values() 中 dict[key] 出现的顺序一致（不管何时，不管做了什么操作）。

Implementation Details
^^^^^^^^^^^^^^^^^^^^^^

CPython 使用 hash tables with preudo-random probing 实现 dictionaries。hash table 我懂，不过 preudo-random probing 是什么
算法。

只有 hashable 的 objects 能做 dictionaries 的 key。

An object is hashable if it has a hash value that never changes during its lifetime and can be compared to different
objects. Every Python's built-in type that is immutable is also hashable. Mutable types such as list, dictionaries, and
sets are not hashable and so they cannot be used as dictionary keys. Protocol that defines if a type is hashable
consists of two methods:

    #. \_\_hash\_\_
    #. \_\_eq\_\_

两个相等的 object 应该具有相同的 hash 值。

CPython 使用 **open addressing** 的办法去解决 collisions(冲突)。我忘记什么是 **open addressing** 了。

自定义 hash 值时要小心， hash 值取得不好，大致 probability of collision 太高的话， hash table 的性能会变得很差的。Java 中常
常用 *31 的方法，算 hash 值，可能 Python 也可以这样写。


使用 **open address**， 那么操作的时间复杂度和加载因子 alpha 是相关的，为什么在 Python 书里，都简单粗暴地说时间复杂度是 O(1),
要想让时间复杂度为 O(1) ， 必须保证实现 dictionaries 的 hash table 表足够大。那么 CPython 实现 dictionaries 的 hashTable 到
底有多大。而且使用 **open address** 的话，如果实际要填的项，大于 hash Table 的大小，是会报错的，CPython 对于这个报错，有没
有特殊的处理？？？

Operation Average complexity Amortized worst
case complexity
Get item O(1) O(n)
Set item O(1) O(n)
Delete item O(1) O(n)
Copy O(n) O(n)
Iteration O(n) O(n)

最差时间复杂度是 O(n) 容易理解，但是平均时间复杂度是 O(1), 明显是假设了实现 dictionaries 的 HashTable 足够大。

还有一点要注意的是，CPython 是如何实现删除 key 的操作的？我猜是这样处理的，就是每个 hashTable 的 slot 都添个 flag 表示是否还
有效。删除某个key,就是修改flag,说明这个 key 无效了。以此实现删除。我猜的这种做法，刚好解释了最差时间复杂度O(n) 中的 n 为什么表
示的是添加过的所有 key 的个数，而不是当前 key 的个数。


Weakness and alternative
^^^^^^^^^^^^^^^^^^^^^^^^

dict 不会以 key 添加的顺序，iter dict。要想以 key 添加的顺序 iterate dict, 需要使用 `OrderedDict`。

dict 可是现实 set(之前 Python 没有提供 built-in 的 set, 导致历史代码会用 dict 实现 set)。现在不要自己用 dict 实现 set, 因为
built-in set 做了不少优化，比自己现实的 set 要快。

Sets
----

Python 提供了 set 和 frozenset, set 是 mutable 的， frozenset 是 immutable hashable 的。

可以通过如下方式构造 set

    .. code-block::

        # construct set.
        set([1, 2, 3])
        {i for i in range(100)}
        {1, 2, 3}

        # construct frozen set.
        frozenset([1, 2, 3])
        frozenset({1, 2, 3})

Implementation Details
^^^^^^^^^^^^^^^^^^^^^^

大体上和 dictionaries 一样都是用 hash table 实现的。不过不要自己去实现 set 。


Beyond basic collections – the collections module
--------------------------------------------------

collections package 提供了扩展的 list, dict, set, tuple 类型。如果要自定义扩展 list, dict, set 和 tuple 的类，应该先去
collections package 中找找有没有现成的。collections 中常用的类型：

* namedtuple（可以用 attribute name 访问数据，不必使用 index 访问）
* OrderedDict（能保持添加 key 的顺序）
* defaultdict（能给 key 赋默认的 value）
* deque(这是用双向链表实现的，如果用队列，请使用 deque, 不要用 list)
* Counter(很有意思，会统计 list 中每个 element 出现的次数)
* ChainMap(todo: 没用过，不理解，为什么要用这玩意)


---------------
Advanced Syntax
---------------


Iterators
---------

iterator protocol: 实现下面两个方法的就是 iterator:

#. \_\_next\_\_ return next item of the container.
#. \_\_iter\_\_ return the iterator itself.


The yield statement
-------------------


yield 用于生成 generator 和 coroutine。常用的方法是 next(generator/coroutine) 和 coroutine.send(msg)。

有的书把 coroutine 也称为 generator。

generator 除了 next 和 send 常见用法外，还有

#. throw 抛异常
#. close 停止迭代

方法可用。


Decorators
----------

Decorators 就是在要包裹的 code 前后包装些代码去执行。

.. code-block::

    @decorator(decorated_code)
    # 上面这句等价于
    decorated_code = decorator(decorated_code)


decorator 可以写成函数，可以写成类，可以带参数。


decorator 一般都需要保持被包装函数的 metadata, 一般使用 functions.wraps 保持函数 metadata。（decorator 可以装饰类，但是没有
现成的工具保持类的 metadata。所以类的 metadata 编程还是使用 metaclass 比较方便）。


Usage and Examples
^^^^^^^^^^^^^^^^^^

#. Argument checking
#. Caching
#. Proxy
#. Context Provider



Context managers - the with statement
-------------------------------------

只要一个类实现了

#. \_\_enter\_\_
#. \_\_exit\_\_

方法，就可以当做 Context Manager 使用

不过 Context Manager 一般都是用 contextlib.contextmanager decorator 实现，明显这种方式更简洁。


我之前忽略了对于异常的处理。

.. code-block::

    # 我一直认为 __exit__ 相当于 finally 而 finally 不做不到异常。看来我错了。
    __exit__(self, exc_type, exc_value, traceback)


同理 @contextmanager decroator 也可以捕获到异常。对于 @contextmanager 我有误解，比如如下代码

.. code-block::

    from contextlib import contextmanager


    @contextmanager
    def f():
        print('start')
        yield
        print('end')


对于上面的代码，我错误的以为 `print('end')` 一定会执行，其实不是这样的，还是必须要 finally clause 中的代码才一定会执行。比如写
成

.. code-block::

    from contextlib import contextmanager


    @contextmanager
    def f():
        print('start')
        try:
            yield
        finally:
            print('end')

这样写的话，`print('end')` 一定会执行。



contextlib 除了最常用的 `contextmanager` decorator, 还提供了 `closing(element)`（生成 contextmanager ，离开 contextmanager
会自动执行 element.close()，可以防止你忘记执行 close()）， `supress(*exceptions)`(生成 contextmanager , 并自动吞掉
contextmanager 中出现的 exceptions)， `redirect_stdout(new_target)`（能把原本要写到 stdout 的字符串，写到 new_target(
file-like object) 中），`redirect_stderr(new_target)`(和 `redirect_stdout(new_target)` 用法类似)。



Other syntax elements you may not know yet
------------------------------------------


#. The for ... else clause
#. Function annotations

这两种语法，我个人意见是少用，太少见。
