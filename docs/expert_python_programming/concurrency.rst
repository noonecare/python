Why Concurrency
===============

* 更高效率
* 更快的响应


multithreading & multiprocessing
--------------------------------

thread 最重要的是要保证访问公共资源时，不会出现竞争。为了达到这个目的，可以加锁。可以使用现成的 threadpool, 可以使用 queue, 用
生产者消费者模型管理等等。

《expert python programming》 使用 token bucket algorithm 实现了 Throttle。算法可以这样理解，如果worker 执行的操作足够快，那
么明显，token bucket algorithm 能够实现限速（限制速度大约等于指定的 rate）的目的。如果 worker 执行的操作不是足够快，可能会是速
度小于指定的 rate，不过你可以提高并发度，来提高速度。

Process 和线程的不同在于有独立的地址空间。

Python 提供了与 Process 相关的操作，比如 fork 等。但是这样的操作太底层一般不用。

Process 提供了 `multiprocessing.Queue`, `multiprocessing.Pipe`, `multiprocessing.sharedTypes` 提供 Queue, Pipe 和共享内存。


不过实际上这些操作都没有直接使用 pool 方便。比如

multiprocessing.Pool 表示进程池
multiprocessing.dummy 表示线程池

这些 Pool 用的比较多。


Asynchronous programing
-----------------------


Asynchronous programming 是 Python 中处理异步IO（尴尬的是 Python 提供的异步IO 优先，比如一直没有特别好的 http 异步IO 包）,
提供更短响应事件最好的机制。


最开始 Python 出现大量的框架，包采用了 Asynchronous programming 方式。Python 吸收了这些框架的方式，在 Python3.5 推出了
asyncio built-in package, 让 Python 原生地支持 Asynchronous programming 的方式。

Python3.5 添加了 `async`, `wait` 关键字， asyncio 提供了内建的调度器，以此实现异步编程。


异步编程就是自己实现调度器。系统级的线程是用操作系统的调度器调度的。操作系统的调度器是可抢占的，调度器可以在线程的任何位置
switch control。而异步编程的调度器是不可抢占的。就是说调度器只能在 coroutine 中预先设计好的位置 switch control。

在异步编程中，重要的点是什么时候交出 CPU 控制权。获得 CPU 是调度器给你的，一般用现成的调度器。


* 是不是默认在读写 IO 时，会交出控制权？

    不是，只有使用异步 IO 时，执行IO 操作会交出控制权。如果使用同步IO，并不会交出控制权。

* 有没有一句代码，可以交出控制权？

    有， await statement, 注意 await 后面跟着的只能是 awaitable 的类型： coroutines 或者 Futures。


* Python3.5 之前，如何实现异步编程？

    在 Python 3.5 之前使用 generator 来写 coroutines。之前的版本把这种 generator 称为 coroutines, 但是之前版本的python 并没
    有定义 coroutine 。知道 Python 3.5 定义了 coroutine，给出了 await 和 async statement, 给出了线程的 scheduler, 这使得不
    必从头开始写 coroutine, 也不必引用第三方包去实现 coroutine。


* 如何把同步IO 变得像异步IO?

    使用线程把同步操作（不过是 IO 操作）转成类似异步的操作。

    Python concurrent.futures 提供了 `Future` 和 `Executor`。

    `Executor` 是抽象类，提供了 `submit`, `shutdown` 和 `map` method。 特别的 `submit` 不会立即执行操作，而是返回 Future 和
    coroutine 非常类似，可以融入异步编程中。

    `Executor` 有两个常用的具体类， `ThreadPoolExecutor` 和 `ProcessPoolExecutor`。

    由此，我们可以把同步的操作伪装成异步操作，融入异步编程中。

    那么这种伪装，对于程序性能有提高吗？

    可能有也可能没有。如果使用 ThreadPoolExecutor 执行 CPU bound Operation，那么对于程序性能几乎没有提升。
    如果使用 ThreadPoolExecutor 执行 IO bound Operation, 由于文件读写一般会调用操作系统的 sys call, sys call 不受 GIL 影响，
    所以能够提高程序的效率。
    如果使用 ProcessPoolExecutor 一般是能提高效率的。

    也就是说，这种伪装能不能提高性能，主要看多线程多进程能不能提高性能。这种伪装主要是用异步编程的写法写多线程多进程。

* 猜测下 async 和 await 的实现？

    我猜 async 可能是在函数体第一行加了 yield，用于交出 CPU 控制权。
    await 也相当于加入了 yield，用于交出 CPU 控制权。

    async 和 await statement 使得写 coroutine 变得简单。不想 Python 3.5 之前，必须手动不断 next, send，必须手动写 loop。唯一
    的劣势是会导致代码和之前的 Python 版本不兼容。


* linux 的 epoll/poll 是否会用在 asyncio 的异步调度器中？

    尚不清楚




《expert python programming》 提了一句 `Blinker`_ 是 Python 中常用的 singal 框架，flask 作者也推荐了 Blinker 有空可以看看。


.. _Blinker: https://pythonhosted.org/blinker/



