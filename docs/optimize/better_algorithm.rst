Reducing the complexity
=======================


有两种广泛使用的复杂度定义

- Cyclomatic complexity, also known as MaCabe's complexity.

    中文称为圈复杂度，之前我从没有听说过圈复杂度。我说复杂度都是指的下面这个复杂度。
    flake8 可以计算圈复杂度，一般认为圈复杂度小于 10 的程序是不复杂的程序。
    圈复杂度就是程序中线性独立路径数（我不喜欢这个定义，因为它又引入了新的概念）。我喜欢以下的定义：

    圈复杂度主要和 if 语句有关。可以根据程序的控制流程图来定义。

    .. math::

        V(G) = e - n + 2 * p, e edge number; n node number; p component number.


    圈复杂度就是控制流程图的区域数，等于判定节点数加 1。

    ? 圈复杂度和 if 语句有关，那么如果我把 if 语句放到 for 循环了，是否这个圈复杂度就成了待定，或者是无穷大。

    .. code-block::

        # a 的长度不定，那么请问这个程序的圈复杂度是多少
        def f(a):
            for a_1, a_2 in a:
                if a_1:
                    print(a_1)
                else:
                    print(a_2)

    使用 flake 计算可知，上面代码的圈复杂度是 3， 就像没有 for 循环一样。

- The Landau notation, also known as big O notation.


Simplifying
-----------

选择合适的数据结构，能够有效地减低复杂度。需要了解 Python 数据的实现。这样可以了解到常用操作的时间复杂度，然后就可以减低
复杂度。

tuple index O(1)
list index O(n)
list 适合 append
dict/set 适合判断存不存在
bisect 对于排好序的序列，找特定元素，使用二分查找，时间复杂度是 O(lgn)
deque 适合做队列
defaultdict 还是要快点。

.. code-block::

    python3 -m timeit -s 'd = {}; d.setdefault("x", None);'
    # 功能上和上一句代码一样，但就是比上一句快
    python3 -m timeit -s 'from collections import defaultdict; d = defaultdict(lambda: None); d["x"]'



除了使用合理地使用数据类型之外，尽量减小 loop 体代码量，也可能能提高效率。

Using architecture trade-offs
-----------------------------


有时候，可以提供近视正确的答案，或者采用异步的方式反馈结果。


- 采用启发式或者近似的算法。

    优化问题，至今都没有算法可以完全避免局部最优解。

    旅行商问题，至今都是 NP 难的。

    提供一个答案，提供这个答案和误差的范围，然后大致就以这个可计算的答案做为答案。
    比如 Simulated annealing, Genetic algorithm, Tabu search, Ant colony optimization, Evolutionary computation 都是启发
    式的算法。


- delay processing

    网路中用的很多，因为网络服务强调响应。可以把一些同座先丢到后台去执行。

    延迟操作常常需要用到消息队列和分布式的任务队列。
    Python 中常用的任务队列有：

    - Celery
    - RQ

    常用的消息队列有：

    - RabbitMQ
    - Kafka


- 使用概率数据结构。

    - HyperLogLog: redis 的核心算法。
    - Blooomfilter

Caching
-------

- 缓存复杂度高的操作，常用的 memorization 算法就基于这个思路。

    Python 有 functools.lru_cache 提供了 last recently used 机制的缓存功能。

- 有时候缓存有时限，比如 session 经常有实现，如何实现由时限的缓存。

    可以自己实现有时限的缓存机制。不过更常见的是使用现成的缓存服务。比如 redis 和 memcached。
    使用 redis 和 memcached 时，最大的问题是如何给出 key, 常用的方式是用 hash 值作为 key, python 中 hashlib 提供了这个功
    能。不过要记住，hash 函数可能会 collision。




