============
Async server
============

:作者: 王蒙
:标签: 网络编程

:简介:

    介绍异步处理 socket 读写的做法。

.. contents::

目标读者
========

网络编程

预备知识
=============

socket 读写数据

问题
=======

定义 async server ？

常见 async server?

async server 的优势和劣势？

解决办法
========


定义 async server ？

    参考 IO models 章节可知。select/poll/epoll 使得 socket 等待数据的步骤（A 步骤）不再阻塞，提高了效率。

    async server 就是使用 select/poll/epoll 处理 socket 读写的 server。

    Python 有很多异步处理 IO 的第三方包（Twisted, Eventlet 等等）。Python 3.5 以来，推荐使用 `asyncio`_ 处理。

    Python `asyncio`_ 提供的抽象，使得我们不必关心该怎么调用 select/poll/epoll。只要

        - 继承 `asyncio.Protocol` 类，定义回调函数，就实现了采用 select/poll/epoll 处理 socket 的服务器。参考 `srv_asyncio1.py`_ 。

        - 直接定义 coroutine, 也能实现 async server 。参考 `srv_asyncio2.py`_ 。补充一句，`srv_asyncio2.py`_ 可以不使用 `asyncio.coroutine` 装饰器。直接写成如下的代码就好

            .. code-block::

                import asyncio

                # async 是 python3.5 提供的定义 coroutine 的修饰符
                async def handle_conversation(reader, writer):
                    ...


    使用 select/poll/epoll 注册了 socket，那么当该 socket 的 outgoing buffer 被填满，是否会使整个程序卡住（CPU 控制权会不会立马交出来）？


常见的 async server ?

    tornado 是 Python 常见的 async server。

async server 的优势和劣势？

    - async server 优势在于性能好，效率高。
    - async server 劣势在于，一般 async server 和 运行在其上的 application 是死死地绑在一起的，不能整出符合 WSGI 的接口。

参考文献
=========

- Foundations of Python Networks Programming

.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _srv_asyncio1.py: https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_asyncio1.py
.. _srv_asyncio2.py: https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_asyncio2.py
.. https://docs.python.org/3.6/library/asyncore.html
.. https://docs.python.org/3.6/howto/sockets.html
.. https://www.scottklement.com/rpg/socktut/nonblocking.html