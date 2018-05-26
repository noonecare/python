============
Async server
============

:Author: 王蒙
:Tags: 网络编程

:abstract:

    介绍异步处理 socket 读写的做法。

.. contents::

Audience
========

网络编程

Prerequisites
=============

socket 读写数据

Problem
=======

怎样异步处理 socket 读写操作？


Solution
========

Python 有很多异步处理 IO 的第三方包（Twisted, Eventlet 等等）。Python 3.5 以来，推荐使用 `asyncio` 异步处理IO。


IO 分为同步IO和异步IO， 异步IO 指的是操作时，立马交出 CPU 控制权，等IO操作结束会产生事件（event）通知程序IO操作已经完成。

socket 的 send, sendall 和 recv 是同步操作，对同步IO 使用异步处理的方式，并不会提高效率。那么是什么操作使得 socket IO 变成了异步操作。





select,poll,epoll 是什么，是不是这些玩意儿把socket IO 变成了异步IO?

    select/poll/epoll + readable()/writable() = 异步 socket IO

    - 每次IO操作前，先判断 readable()/writable() ，这些操作会立马返回 True/False，然后实际 IO 操作会交给 select/epoll/poll 去处理。
    - 每次 IO 操作完成之后，会修改 file descriptor 的 readable, writable 的状态，相当于反馈了 IO 完成的事件。

使用 select/poll/epoll 注册了 socket，那么当该 socket 的 outgoing buffer 被填满，是否会使整个从程序卡住（CPU 控制权会不会立马交出来）？






怎样使用 asyncio 异步处理 socket 读写操作？

    - 继承 `asyncio.Protocol` 类，定义回调函数，就实现了采用异步IO处理方式的服务器。参考 `srv_asyncio1.py`_ 。

    - 直接定义 coroutine, 也能实现采用异步IO处理方式的服务器。参考 `srv_asyncio2.py`_ 。补充一句，`srv_asyncio2.py`_ 可以不使用 `asyncio.coroutine` 装饰器。直接写成如下的代码就好

        .. code-block::

            import asyncio

            # async 是 python3.5 提供的定义 coroutine 的修饰符
            async def handle_conversation(reader, writer):
                ...

Reference
=========

- Foundations of Python Networks Programming

.. _srv_asyncio1.py: https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_asyncio1.py
.. _srv_asyncio2.py: https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_asyncio2.py
.. https://docs.python.org/3.6/library/asyncore.html
.. https://docs.python.org/3.6/howto/sockets.html
.. https://www.scottklement.com/rpg/socktut/nonblocking.html