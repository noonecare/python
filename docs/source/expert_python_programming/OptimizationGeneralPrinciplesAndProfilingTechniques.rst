Three rules of optimization
===========================


- 不要过早优化，先让程序能跑通
- 保持代码的可读性
- 用使用者的观点，看是否需要优化，哪里需要优化，不要没有业务目的地去优化

Optimization strategy
=====================



- 确保应用依赖的服务没错
- 提供足够硬件资源
- 写性能测试


Finding bottlenecks
===================


- CPU Usage

    Macro-profiling: profile 整个程序，找到那几个部分影响性能。

        - cProfile: python 做 profile 的工具。（Profile 和 cProfile, 但 cProfile 比 Profile 强，所以不要用 Profile）

        - pstats 读取 cProfile 产生的 profile 报告。Pycharm 提供了更好的支持。

        - 如何理解 profile 报告。在 Pycharm 下一切很简单。不用写任何附加的代码，直接点 profile , 就会生成可读的 profile
        （包括一张表和一幅图），那个图尤其直观，会显示每个函数的time(总耗时) 和 own(自身耗时，不包括其调用的其他函数的
         执行时间)，会显示耗时占总耗时的百分比。耗时多的函数，会染成红色。


    Micro-profiling: 针对上一步找到的函数，再做 profile 。

        - profile 刚才找到的耗时函数，进一步找出瓶颈。
        - timeit 包能非常简便地测试函数耗时（如果你有 pycharm，使用 cProfile 已经很简单，没有必要用 timeit。如果你用命令
        行操作，timeit 用起来非常简便，尤其是测单行代码的耗时尤其方便）。


        .. code-block::

            $ python3 -m timeit -s 'a = [str(i) for i in range(10000)]'

    Measuring Pystones, 不同计算机 CPU 性能不一样，你的程序在一台计算机上跑得快，不一定说明它在其他机器上跑得也很快。为
    了整体的估计程序在所有计算机上的效率。整出了一套测试作为 benchmark。计算待测试程序的效率表示为几个单位的benchmark。
    python 提供了 pystones 包，pystones 包会计算待测试程序的耗时是几个 pystones。

    我认为就算是同一台机器，程序每次的运行时间不是不变的。比如在 linux 上我完全可以把其他进程的优先级调高，那么这个
    python 程序运行时间就会变长。所以我认为 pystone 绝度不是特别准确的度量方式。

    不同操作系统的进程调度策略不同，也会对程序的运行时间造成印象。

    那么就以 Linux 操作系统为例，当前环境的哪些因素会影响程序的运行时间。




- memory Usage

    Python 程序有自己的垃圾回收机制。但从 Python 代码中不好控制内存使用。

    检查内存泄露的工具： *tracemalloc*, *objectgraph*, *gc*, *weakref* 等检测内存的工具。

    轻易不要自定义 **__del__** 方法，在循环引用中，有的版本的 Python 不能正确地释放自定义了 **__del__** 方法的引用。

    有些情况下，python code 中会有引用（变量名）指向一块内存（变量），但是却不想因为这个变量名增加变量的 referenceCount, 也就是说导当仅有
    这个变量名指向变量时，希望 Python 的 garbage collector 可以回收这块内存。这时候，需要使用 weakref。

    相比于 Python code, Python C extension 更容易造成内存泄露。写 C extension 时，如果你漏写了 *Py_DECREF*，那么就会发生
    内存泄露。所以少跟 Python/C API 打交道，很容易内存泄露。如果不得不写，一定要写测试 C API 是否会发生内存泄露。比如循
    环执行 C API 很多次检测内存占用是否有明显上升。`Valgrind`_ 是检查编译好的代码是否会发生内存泄露的工具，可以了解下。

- network Usage

    IO 也可能影响程序的效率，其中网络 IO 尤为明显。

    书中只是简略地提了提，可能用到的工具。

    - ntop
    - wireshark
    - net-snmp
    - 估计两台电脑之间带宽的工具 Pathrate

    我晕，我一个也没有用过。我用过的工具是 wget/curl/ping/tcpdump。感觉网络这块，得系统的整理下，之前断断续续从 google
    上学到的内容，感觉不成体系。


.. _Valgrind: http://valgrind.org/