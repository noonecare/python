===========
IO Models
===========

:Author: 王蒙
:Tags: 网络编程，异步IO，阻塞IO

:abstract:

    blocking-IO, non-blocking IO, asynchronous IO, synchronous IO 经常遇到，但是经常搞不清楚有什么区别和联系。本节详细介绍这几种IO, 特别是其对于性能的影响。

.. contents::

Audience
========

网络编程，高并发

Prerequisites
=============

socket


Problem
=======

- IO 模型有哪些，它们的区别和联系是什么
- select/poll/epoll 为什么会有好的性能


Solution
========


- IO 模型有哪些，它们有什么区别和联系？

    socket IO 分为两步： A. 等待数据；B. 把数据从内核去拷贝到用户区。IO 模型有以下五种：


        - blocking IO：socket 的读写操作默认是 blocking IO。socket 读写操作需要等 A，B 两步都完成，读写操作才会返回。
        - non-blocking IO：
            - A 步骤没有完成， 立即返回。
            - A 步骤完成了，立即执行 B 步骤。

        - IO multiplexing: select 返回 ready 的 socket（如果没有一个 ready 就会阻塞，具体看下面的 select 函数介绍），用户一般会对 ready 的 sockets 进行 B 步骤。

        - signal-driven IO: A 步骤完成的时，产生信号。信号触发信号处理函数，信号处理函数一般是执行 B 步骤。

        - asynchronous IO: A 和 B 步骤都完成时，产生信号，触发信号处理函数。POSIX 提供 aio_XXX API, 不过几乎不用。可以查看 `what is the status of posix asynchronous io aio`_ 。

        .. image:: ./IO_models.png


    .. code-block::

        # socket is blocking by default.
        sock = socket(AF_INET, SOCK_STREAM)
        # blocking by default.
        sock.recv()
        sock.send()
        sock.sendall()
        sock.connect()
        sock.accept()

        # set opts to be non-blocking IO.
        sock.setblocking(False)
        # return not ready immediately, or begin to copy data from kernel to user.
        sock.recv()
        sock.send()
        sock.sendall()
        sock.connect()
        sock.accept()

        # IO multiplexing
        # select/poll/epoll will check whether socket is ready.
        for fd, event in select(read_fds, write_fds, exception_fds, timeout):
            fd.write(b'blablabla')


        # signal-driven IO. 很少用在 TCP 中， 需要提前注册 SIGIO 的事件处理函数。参见 Unix Networks Programming Volume 1, 25.2 Signal-Driven I/O for Sockets 节


- select/poll/epoll 为什么有好的性能？


    - select/poll/epoll 高效地返回已经ready的文件描述符，对这些文件描述符可以直接执行B步骤。

        There are three possibilities:
            #. Wait forever— Return only when one of the specified descriptors is ready for I/O. For this, we specify the timeout argument as a null pointer.
            #. Wait up to a fixed amount of time— Return when one of the specified descriptors is ready for I/O, but do not wait beyond the number of seconds and microseconds specified in the timeval structure pointed to by the timeout argument.
            #. Do not wait at all— Return immediately after checking the descriptors. This is called polling. To specify this, the timeout argument must point to a timeval structure and the timer value (the number of seconds and microseconds specified by the structure) must be 0.


    - select/poll/epoll 是不是无限循环调用 socket 的 is_readable(), is_writable() 方法来检查socket 是否 ready 的？ 我百分之百的确定不是。

    - select 的实现？

        select 函数对于每个监测的文件描述符，调用该文件描述符（设备，需要设备驱动的支持）的 poll 方法，poll 方法负责检查文件描述符是否 ready。现在操作系统，一般是用中断来通知处理IO的。所以 poll 方法是通过中断，而不是通过轮询来获知文件描述符是否 ready。

        poll 方法做的操作，简单讲是把相关进程添加到等待序列中，当要等待的IO 事件发生后，等待序列中的进程会被 wake up（如果进程在 sleep 的话）。

        要百分百整清楚 select 的实现，可以去看 select 的源码。对于性能层面的东西，一定会涉及操作系统。要百分百具体的看到底层的实现，需要看操作系统的源码，这对 C 语言以及操作系统的知识要求很高，需要慢慢来，捡重点看。






Reference
=========

- Example: Using asynchronous IO: https://www.ibm.com/support/knowledgecenter/en/ssw_i5_54/rzab6/xasynchi0.htm
- How is select implemented: https://www.quora.com/Network-Programming-How-is-select-implemented
- Operating System Concepts
- Linux Device Drivers


.. _what is the status of posix asynchronous io aio: https://stackoverflow.com/questions/87892/what-is-the-status-of-posix-asynchronous-i-o-aio
