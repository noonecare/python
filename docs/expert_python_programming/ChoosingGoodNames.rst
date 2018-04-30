PEP 8 and naming best practices
===============================

我仔细读过 `PEP 8 文档`_ ，所以这部分略。


Beyond PEP 8 - team-specific style guidelines
---------------------------------------------



Name styles
-----------

Naming and Usage
----------------

这里说，为什么要用复杂的配置的文件，用 settings.py 做配置文件不好吗？

我无言以对。除非用到第三方工具，比如 docker 需要写 docker-compose.yml, tox 需要写 tox.ini 外，简单的配置文件写成 settings.py
就很好了。我学的东西已经非常全面了，决定学习新东西之前，可以先问问自己，值不值了。


Public and private variables
----------------------------

《expert python programming》 反对使用 name mangling 。


Functions and methods
---------------------

The Private controversy
-----------------------

Special methods
---------------

`Special methods`_


The naming guide
----------------


#. Using the has or is prefix for Boolean elements.
#. Using plurals for variables that are collections.（英文名词有单数和复数，用复数名词表示 collections, 比如下面的代码。我
想了好几分钟，到底 1 + i 这个复数和代码规范有什么联系，后来，我明白了，是英文名词的单复数）
#. Using explicit names for dictionary.
#. Avoid Generic Names. （Generic Names 不能反映标识符表示什么含义，标识符应该表明用途，越具体越好， 书中举了写例子， 不要用
`compute`, `handle`, `do`, `manager`, `object`, `perform`, `misc`, `tools`, `common`, `core`, `utils`。这几个例子，挺让我
震惊的，因为我他妈一直以为用 utils 命名显得代码很规范。不过现在我觉得书中说的是读的，我认为总体上，如果没有提供有用的信息，那么
越简洁越好。）
#. Avoid Existing Names. （会让人迷惑，变量到底代表什么含义。可以用添加 trailing underscore 的办法避免名称重复）


Best practices for arguments
----------------------------

#. Build arguments by iterative design

    首次写，一般不可能把 arguments 写的特别完美，可能之后还需要完善。在完善的时候，如果是添加 argument，那么最好设置默认值，使
    得不必修改使用该 API 的代码。
    如果原来的 API 非改不可。那么 ...

#. Trust the arguments you tests

    Java 中常常会使用 `assert` 检验 `*args` 和 `**kwargs` 的有效性。但是《expert python programming》 的作者认为对于 Python
    不要怎么做。

    该书作者认为：

        #. 明确指明函数该如何使用，降低了代码的可读性。（好吧，我一直认为是提高了可读性。）
        #. 会使程序运行地更慢。（好吧，Effective Java 说对于不合理的参数，早退提高了程序的效率。）

    《expert python programming》 Python 输入有效性，不应该靠函数开头的 `assertion` 语句，而应该靠代码的测试用例来表现。这一
    点，我同意。因为读源码时，我从来不指望Python 提供参数的类型信息，所以我总是先看实际使用的例子（Doctest 做测试，一般会给出实
    际用例），或者是测试用例。

    而读 Java/Scala 代码，我总是先看 API 输入参数的类型，常常能推测出些信息。

    我认为可能是因为 API 的使用者，更倾向于读测试用例，读文档来了解 API 的用法。使得在 Python 中 assert 来检验 `*args` 和
    `**kwargs` 的方法吃不开。另外 Python 设计理念中有一句： 假设 API 用户都是负责的用户。因为用户负责任，所以用户传给 API 的参
    数都是合法的。

    不管怎么讲，我并没有体会到 assert 减低代码可读性，使得程序变慢。可能这是我没有体会到的点。

#. Use \*args and \*\*kwargs magic arguments carefully


    **Concise and Precise** 的要求，不要搞得太抽象。



Class names
-----------


    A Common practice is to use a suffix that informs about its type or nature, for example:

    #. SQLEngine
    #. MimeType
    #. StringWidget
    #. TestCase

    For base or abstract classes, a **Base** or **Abstract** prefix can be used as follows:

    #. BaseCookie
    #. AbstractFormatter

    这说的有点想李萌之前说的，用类型后缀，不过李萌太过了，简单的变量名也要加后缀就显得复杂了。

    方法名不必包含类名中包含的语义，显得繁琐。比如

    SMTP.smtp_send() 写成 SMTP.send() 更好，因为 smtp_send 的 `smtp_` 不包含任何新的语义。

Module and package names
------------------------

module 名和 package 名常常很短，全小写且不加下划线。

如果一个包实现了一个协议，一般会有 lib 后缀。

一般会在包的 `__init__.py` 文件中提供更便捷的使用路径，用 import 的方式。


Useful Tools
------------


#. Pylint

    这个工具很有趣，会给代码打个分数，评判代码的质量（当然只是 code style 的质量）。我测了下我写的 40 来行的代码，我觉得写
    的非常棒，结果只得了 6 点几分。我测了我两个同事的代码，一个得到 3 分，一个得了 -3 分。我又试了下 flask 源码，得了 7.79
    分。logging 得分 7.23 分，asyncio 7.96 分。这个分数很神奇。《expert python programing》 中说这个分数并不重要，但是我
    感觉还是大概其能估计出代码 code style 质量的， 比如我感觉代码得分在 7 分就算是优秀的代码。

    我认为这个分数还是有点用的，除此之外更重要的是， pylint 会告诉你哪一行代码，因为什么原因不规范。可以根据它的提示改。

    最后， pylint 可以自己定制代码规范标准，对有特殊规范的开发团队会有用。

    我感觉 pylint 默认使用的代码规范并不是 pep8 。


#. pep8

    这个就是用 pep8 规范，检查代码，报告哪些代码写的不规范。

#. flake8

    这个除了提供 pep8 的功能，还提供了其他功能，有名的有：

    #. 计算代码的圈复杂度
    #. 使用 comment 跳过代码规范检查，比如 # noqa 相当于告诉 flake8 ，我知道我不规范，但是不要检查我。
    #. Static analysis via pyflakes 不明白这个东东是什么意思


这些代码检查工具，常常会放到 CI 流程中，检查代码质量。


总结：

    规范上，我认为基本原则是 **concise and precise**，就是说变量名包括变量名的格式，要能表现出变量的含义，变量的用法。如
    果有一种更冗长的方式，没有包含更多的语义信息，那么这种方式应该舍弃，改使用更简洁的方式。








.. code-block::

    tables = ['product', 'price', 'sale']









.. _PEP 8 文档: https://www.python.org/dev/peps/pep-0008/
.. _Special methods: https://docs.python.org/3/reference/datamodel.html#special-method-names