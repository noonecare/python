===========
Concurrency
===========

:Author: 王蒙
:Tags: 并发

:abstract:

    讨论并发，Python 并发。

.. contents::

Audience
========

Python 开发

Prerequisites
=============

Problem
=======

- 多线程 & 多进程
- 异步IO
- 信号

Solution
========

多线程&多进程
~~~~~~~~~~~~~~~~~~~~~~~~~~

线程和进程

- 线程和进程都是操作系统的概念。
- 线程和进程最大的不同在于，多个线程同属于同一个进程，可以共用该进程的公共变量。不同进程有不同的地址空间，不会共享变量（现代操作系统为了实现进程间通信，可以声明允许多个进程访问的 Shared data，但是默认不同进程是不能共享变量的）。
- 进程和线程在 CPU 切换控制权时，都需要切换上下文(switch context)，一般线程 context switch 比进程的 context switch 耗时小。


如果要解决的问题可以完全拆分成多个完全独立的任务。那么多线程多进程编程非常简单。
但是实际问题，通常需要多个线程进程之间访问同一些变量(competition)，或者多个进程之间有协作（cooperative）。

为了协调(synchronize)多线程多进程，使得多线程多进程可以协作和竞争。程序设计语言提供了两种机制：

    - Semaphore: 信号量。Semaphore 就是多个线程都能及时看到的变量，根据 Semaphore 的状态，确定是否能够访问资源。就是说多线程多进程实现同步是由当前的编程者来实现。Semaphore 就是常说的 Lock，就是用 Lock 包围一部分代码。只有在 Lock 满足一定条件时，被包围的代码才能执行，否则被包围的代码需要等待。

    - Monitor: 中文一般翻译为监视锁。在写抽象数据类型时，把公共访问的资源放到该数据类型内部，该数据类型对外提供接口去访问要公共访问的资源。这些接口实现（基本上也是通过 Semaphore 来实现）了同步访问公共资源的功能。由此使得该数据类型 thread Safe。

    Semaphore 和 Monitor 其实是写多线程多进程代码的两种方式，一种方式是把同步多线程多进程的工作交给类库使用者去做，一种是交给类库作者去做。写类库时，涉及到多线程多进程，一定要注明方法是不是 thread safe 的。

多线程不容易调试，易出错。所以尽量使用 Monitor( thread safe 的数据类型)，避免自己手动写多线程导致出错。

为了减轻线程调度的负担，也为了提高效率（创建销毁线程是比较耗时的操作），现代程序设计语言（比如 Python, Java）都把任务和线程池分离。定义好的任务可以用现成的线程池执行。线程池有现成的线程调度策略可选。


Python 多线程和多进程
~~~~~~~~~~~~~~~~~~~~~~~~~~

Python 多线程多进程最大的特点是 GIL 全局锁。Python 代码在执行时由于全局锁的存在，每个Python进程只能占用一个线程。这导致 Python 多线程没办法发挥多核的性能优势。Python 进程不受 GIL 影响，可以使用多核。Python C extension 可以使用多核，Python 调用的 sys call 当然也可以使用多核。所以 IO bound 使用多线程能提高性能，但是对于 CPU bound 使用多线程没有帮助。

Python 多线程多进程的另一个特点，就是会以 context manager 的语法写锁，写 pool。比如：

.. code-block::

    with Lock():
        ...

    with Pool(POOL_SIZE) as pool:
        results = pool.map(fetch_place, PLACES)


其他方面，Python 的多线程多进程和其他语言非常类似。这里主要介绍下 Python 哪些包，哪些数据类型提供了多线程多进程相关的功能：


`threading`

    - Thread 表示线程
    - Lock 代表锁

`multiprocessing`

    - multiprocessing.Pool 表示进程池。
    - multiprocessing.dummy 表示线程池。
    - `multiprocessing.Queue` 提供了用于进程的 Queue ，常用于实现生产者消费者模型。
    - `multiprocessing.Pipe` 提供了管道，进程通过管道把数据传递给另一个进程。
    - `multiprocessing.sharedTypes` 提供了共享内存。

`queue`

    - queue.Queue 线程安全的队列，常用于生产者消费者模型。queue.Queue 注意 `task_done()` 和 `join()` 方法。

`concurrent`

    - `concurrent.futures`: futures 代表将来会用线程或者进程执行的任务，现在该任何可能执行完了，也可能没有执行完。
    - `concurrent.futures.ThreadPoolExecutor`: submit 方法返回 futures。
    - `concurrent.futures.ProcessPoolExecutor`: subumit 方法返回 futures。

此外 Python 的 list, dict, tuple 等基础类型是线程安全的。


线程中执行 sleep(10) 时，该线程是否会交出 CPU 控制权?

    线程调度是抢占性的，操作系统调度器可能在任何时候，抢走 CPU 控制权。

    sleep(10) 是说当前线程在 10s 之后执行，注意这里不是说 10s 的 CPU 时间，而是说 10s 的墙上时间。

    sleep(10) 本身不会主动交出 CPU 控制权。


异步编程
~~~~~~~~~~~

多线程能提高处理IO bound 程序的性能，但是异步编程是更好的办法，因为线程 context switch 要花时间，异步编程不需要花这部分时间；因为异步编程不需要限制对于公共资源的访问。

Python 异步编程使用 coroutine 来定义，需要自定义或者使用Python 提供的调度器。coroutine 会使用 await 语句(Python3.5 之前是通过 yield 语句)交出 CPU 控制权给调度器，调度器负责调度多个 coroutines 的执行。

自定义实现的调度器是非抢占的，而多线程多进程的调度器是抢占的。就是说 coroutine 只会在预先设计好的（await 语句或者 yield 语句）地方交出 CPU 控制权，调度器没法从其他地方抢走CPU控制权。

Python 3.5 之前没有 coroutine 类型，需要使用 generator 来定义一个 coroutine。Python3.5 添加了 `async`, `await` 关键字， asyncio 提供了内建的调度器，这使得异步编程变得简单。

Python3.5 的 async 和 wait 语句：

    - async: 定义函数时，加上 async 修饰符，定义的函数会返回 coroutine。
    - await: await 会交出 CPU 控制权。注意 await 后面跟着的只能是 awaitable 的类型： coroutines 或者 futures。


Python3.5 之前，如何实现异步编程？

    之前使用 generator 来定义 coroutine。比如下面的例子。

    .. code-block::

        def f():
            x = yield
            print(x)

        c = f()
        next(c)
        c.send(1)


如何把 blocking IO 变得像 non-blocking IO ?

    可以使用多线程多进程把 blocking IO 整成 non-blocking IO。

    Python concurrent.futures 提供了 `Future` 和 `Executor`。

    `Executor` 是抽象类，提供了 `submit`, `shutdown` 和 `map` 方法。 特别的 `submit` 不会立即执行操作，而是返回 future ，future 可以用在 await 之后，以此融入异步编程中。

    `Executor` 有两个常用的具体类， `ThreadPoolExecutor` 和 `ProcessPoolExecutor`。


信号
~~~~~~~~~

系统信号

    signal 包提供了信号量，不过不同操作系统的信号量不一样，这可能导致代码没法兼容所有操作系统。

    signal(signal_value, handler) 注册信号处理函数。
    os.kill(pid, signal) 向 pid 进程发送 singal 信号。
    os.killpg(pgid, sid) 向 pgid 进程组发送 sid 信号。

自定义信号

    `Blinker`_ 可以自定义信号，实现异步。

    .. code-block::

        from blinker import signal

        # 定义信号
        zhaoqiaoxinmei = signal('zhaoqiaoxinmei')

        # 定义信号处理函数
        def qimunanxiong(s, **kwargs):
            print("你就是神明眷顾的女孩")
            print(kwargs['reply'])
            print("有空聊")

        # 绑定信号和信号处理函数
        zhaoqiaoxinmei.connect(qimunanxiong)

        # 发出信号，信号中带数据
        zhaoqiaoxinmei.send(None, reply="嗯嗯，有点事儿")



Reference
=========


- 程序设计语言概念 Chapter 13 concurrency
- Blinker 官方文档： https://pythonhosted.org/blinker/
- Expert-Python-Programming Chapter 13 concurrency
- Python 3.5 之前的 coroutine 写法： http://www.dabeaz.com/coroutines/Coroutines.pdf
-


.. _Blinker: https://pythonhosted.org/blinker/