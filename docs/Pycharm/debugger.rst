===========
debugger
===========

:作者: 王蒙
:标签: debug, 调试

:简介:

    介绍 Pycharm 的 debug 功能。

.. contents::

目标读者
========

使用 Pycharm 的开发人员

预备知识
=============

线程，断点

问题
=======

- 断点
- 单步执行
- Resume Program
- watcher & evaluator

解决办法
========

断点

    除了基本的操作（参见参考文献中的视频），可以设置 **条件断点** 。

    调试多线程的程序，可以设置断点是仅仅 suspend 当前线程的执行，还是 suspend 所有线程的执行。

    .. image:: ./断点.png

    Alt + 2 能查看所有的断点，书签。在调试程序和阅读源码时，会很方便。

单步执行

    step over

        把调用函数（包括执行函数定义中的每一句，函数返回）看成一步。

    step into

        把调用函数看成多步，会进入到函数定义中（进入函数定义中后，可以接着单步执行执行函数定义中的每一步）。

    step out

        一步执行完当前函数（或者模块）剩余的所有语句。

    step into my code

        不进入第三方包的函数定义。但是会进入自己的函数定义。

Resume Program

    运行到下一个断点处。

watcher & evaluator

    evaluator 可以在断点处执行代码，调试程序。
    watcher 可以观察各个变量的值。


参考文献
=========

- Pycharm Debug: https://www.youtube.com/watch?v=QJtWxm12Eo0&t=5s
- Stepping Through the Program: https://www.jetbrains.com/help/pycharm/stepping-through-the-program.html#tips-tricks
