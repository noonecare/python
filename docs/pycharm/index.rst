================
Pycharm
================

:作者: 王蒙
:标签: IDE

:简介:

    介绍 Pycharm 。

.. contents::

目标读者
==========

Pycharm 用户

预备知识
=============


问题
=======



解决办法
==========

Pycharm 超好用功能
-------------------------------

调试器（debugger）
^^^^^^^^^^^^^^^^^^^^^^^

    断点

        除了基本的操作（参见参考文献中的视频），可以设置 **条件断点** 。

        调试多线程的程序，可以设置断点是仅仅 suspend 当前线程的执行，还是 suspend 所有线程的执行。

        .. image:: ./断点.png

        Alt + 2 能查看所有的断点，书签。在调试程序和阅读源码时，会很方便。

    单步执行

        step over

            把调用函数看成一步。

        step into

            把调用函数看成多步，会进入到函数定义中（进入函数定义中后，可以接着单步执行函数定义中的每一步）。

        step out

            一步执行完当前函数（或者模块）剩余的所有语句并返回。

        step into my code

            不进入第三方包的函数定义。但是会进入自己定义的函数定义。

    Resume Program

        运行到下一个断点处。

    watcher & evaluator

        evaluator 可以在断点处执行代码，调试程序。
        watcher 可以观察各个变量的值。

    Run Config: 参见视频 `Running Python Code`_ 。

        - Interpreter: vagrant, ssh, docker, local interpreter。

        - Run configuration。

编辑器（editor）
^^^^^^^^^^^^^^^^^^^^^^

    具体看 `Code Navigation`_ 视频。

        - 查找

    具体看 `Productive Coding`_ 视频。

        - 重构（refactor）。
        - 自动补全, Alt + Enter 键。
        - 模板（template）。
        - language injection。

git
^^^^^^^^^

    Pycharm 使用 git 相比于直接使用命令行的优势在于：

        - 可视化的界面显示了提交了哪些更改。

        - 方便和 Pycharm 的其他功能集成。比如可以设置在 git 提交代码之前先检查代码，代码不规范不能提交等。


数据库，科学计算和网络开发
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Pycharm 提供了图像化的数据库使用界面。

    提供了科学计算模式，画图表时，会略微方便一点。

    对 Django 的支持相当好。

    具体的参考 `What's New in Pycharm 2017.3`_ 。


部署
^^^^^^^^^^

    vagrant, docker, remote interpreter Pycharm 都支持。

    Tools -> Deploy  upload 功能，可以方便地把代码部署到服务器上。

检查代码
^^^^^^^^^^^^^^^^

    我一般用 pylint, flake8 不怎么用 Pycharm 的 Inspect code 功能。

Terminal
--------------------

Pycharm 几乎提供了开发相关的所有功能。而且 Pycharm 可以配置 Tools -> External Tools ， 让 Pycharm 集成命令行工具。但除了上一节介绍的功能之外，我选择直接使用命令行。

如图配置 terminal 为 bash.exe（安装了 git 就会有 bash.exe, 该 bash.exe 会启动类似 unix 的命令行环境）。这样配置之后，就可以以 unix 命令行的方式使用各种工具（比如 git,fabric,pylint,pytest,sphinx，coverage,profile）做开发。

.. image:: ./terminal.png


Pycharm 通过安装 plugins （比如 docker, maven, markdown, redis 等等插件）扩展功能。坑爹的是，JetBrains 的 plugins 源有时候访问不了，下不来插件。


常用快捷键
----------------------

- Ctrl + Shift + A: 寻找 Pycharm 提供的功能

- Alt + Enter： 自动补全

- Ctrl + F7： 查看 Usage

- Shift + Shift: 搜索类，字符串等等。

- Ctrl + R: 替换

- Ctrl + Z: 撤销

- Ctrl + /: 注释/撤销注释

- Ctrl + Alt + L : Reformat code。

- Ctrl + Q: 查看文档。

- Ctrl + P: 查看函数的 signature。

- Ctrl + K: 提交代码。

- Ctrl + W: 选择代码块。

- Ctrl + -: 折叠代码块。

- Ctrl + =: 展开代码块。

- Ctrl + B: 查看函数，类的实现。

- Ctrl + O: 查看基类的方法。

- Alt + 1: 查看 project 结构。

- Alt + 2: 查看书签和断点。

- Alt + 6: 查看 todo。

其他
-------------

学会使用 Pycharm, 基本就会使用 JetBrains 公司出的其他 IDE。包括 Intelij IDEA, WebStorm, Clion 等等。

不使用 IDE, 纯手写（比如用纸和笔写代码）更提高代码水平。比如：

    - 实现算法的时候，手写代码。
    - 代码不依赖第三方包时，手写代码（更能体会编程语言本身的特性）。
    - 预先写伪代码。简单的代码看不出伪代码的好处，但是如果项目复杂，提前写好伪代码，能避免很多坑。
    - 最后，手写代码对面试帮助非常大。

单说开发效率，我坚持认为 Pycharm 能大大提高开发效率。

订阅 youtube 上的 JetBrainsTV 号，这个号里有大量的视频教程。

看 Pycharm help 文档，文档中详细写了每个功能的用法。



参考文献
=========

- Pycharm Debug: https://www.youtube.com/watch?v=QJtWxm12Eo0&t=5s
- Stepping Through the Program: https://www.jetbrains.com/help/pycharm/stepping-through-the-program.html#tips-tricks
- Running Python Code: https://www.youtube.com/watch?v=JLfd9LOdu_U&list=PLQ176FUIyIUZ1mwB-uImQE-gmkwzjNLjP&index=4
- Code Navigation: https://www.youtube.com/watch?v=jmTo5xTRka8&list=PLQ176FUIyIUZ1mwB-uImQE-gmkwzjNLjP&index=6
- Productive Coding: https://www.youtube.com/watch?v=XOkNJxvNtPw&list=PLQ176FUIyIUZ1mwB-uImQE-gmkwzjNLjP&index=5
- What's New in Pycharm 2017.3: https://www.youtube.com/watch?v=OHwh0c8UsW4&t=148s
- 10 Essential Tips and Tricks For Intelij IDEA: https://www.youtube.com/watch?v=Mr2mPu1tLhk
- Pycharm help 文档：https://www.jetbrains.com/help/pycharm/meet-pycharm.html

.. _Code Navigation: https://www.youtube.com/watch?v=jmTo5xTRka8&list=PLQ176FUIyIUZ1mwB-uImQE-gmkwzjNLjP&index=6
.. _Productive Coding: https://www.youtube.com/watch?v=XOkNJxvNtPw&list=PLQ176FUIyIUZ1mwB-uImQE-gmkwzjNLjP&index=5
.. _What's New in Pycharm 2017.3: https://www.youtube.com/watch?v=OHwh0c8UsW4&t=148s
.. _Running Python Code: https://www.youtube.com/watch?v=JLfd9LOdu_U&list=PLQ176FUIyIUZ1mwB-uImQE-gmkwzjNLjP&index=4