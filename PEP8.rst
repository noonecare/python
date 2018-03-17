我认为中文版的 PEP8 翻译的很烂，所以我翻下 PEP8 规范。

========================================
PEP 8 -- the Style Guide for Python Code
========================================

正式的 PEP 8 规范由 Kenneth Reitz 编写。

=====
简介
=====

本文档给出 python 标准库遵守的代码规范。

本文档和 PEP 257（文档字符串规范）主要采纳了 Guido 写的 Python 代码规范， 同时也从 Barry 的代码规范中借鉴了一些。

代码规范随着时间会不断改变，因为不断有新的代码规范加进来， 同时旧的代码规范也可能被淘汰。

很多项目有项目自身的代码规范。 当项目代码规范和本文档的代码规范矛盾时，请优先采用项目自身的代码规范。


=======================================================================
不要死守规范（ A Foolish Consistency is the Hogoblin of Little Minds）
=======================================================================

Guido 最重要的发现就是： 代码更多是用来读的。 本文档的代码规范主要是为了提高代码的可读性，让所有 Python 代码都整齐划一。 正如 PEP 20 所说， 可读性不容忽视。

风格规范的重点是一致性。 一定要确保代码风格一致，至少在一个项目，一个模块内部要保证一致性。

有时候，各个代码规范会发生冲突。这时候要靠自己灵活处理。如果拿不定主意，可以参考别人的代码。不要不好意思问别人。

特别地， 不要为了代码风格一致，破坏了代码的后向兼容性。

当出现以下几种情形时，可以无视代码规范：

#. 当采用代码规范不能提高代码可读性时。
#. 由于历史原因，采用代码规范会使得代码与历史代码风格迥异时。
#. 代码在相关代码规范出现之前就写好了，现在再改意义不大。
#. 代码需要兼容老版本的 python ，老版本 python 不支持准备采用的代码规范时。


========
代码布局
========

----
缩进
----

每次缩进，使用 4 个空格。

连续代码（一行代码很长，需要分在多行写）中被裹着的代码（可能被 (), [], {} 包裹）应该垂直（左）对齐；或者采用悬挂缩进。使用悬挂缩进时，要注意： 连续代码的第一行不能有参数，后面的几行代码要有更多的缩进以明确显示代码行是连续代码。

Yes::

    # Aligned with opening delimiter.
    foo = long_function_name(var_one, var_two
                             var_three, var_four)

    # More indentation included to distinguish this from the rest.
    def long_function_name(
            var_one, var_two, var_three,
            var_four):
        print(var_one)

    # Hanging indents should add a level.
    foo = long_function_name(
        var_one, var_two,
        var_three, var_four)

No::

    # Arguments on first line forbidden when not using vertical alignment.
    foo = long_function_name(var_one, var_two,
        var_three, var_four)

    # Further indentation required as indentation is not distinguish.
    def long_function_name(
        var_one, var_two, var_three,
        var_four)
        print(var_one)



连续代码中的缩进不必非用 4 个空格不行。

Optional::

    # Hanging indents *may* be indented to other than 4 spaces.
    foo = long_function_name(
      var_one, var_two
      var_three, var_four)


当 if 中的条件表达式很长，必须写成多行代码时，使用括号包裹条件表达式。这时候 if 加上空格再加上左半边括号，刚好四个字符。if 语句内的语句也缩进 4 个空格，
导致条件表达式和 if 语句内的语句看起来很像，容易混淆。 PEP 8 对于这种情况没有明确说明，以下几种处理方法都可以接受::

    # No extra indentation.
    if (this_is_one_thing and
        that_is_another_thing):
        do_something()

    # Add a comment, which will provide some distinction in editors
    # supporting syntax highlighting.
    if (this_is_one_thing and
        that_is_another_thing):
        # since both conditions are ture, we can frobnicate.
        do_something()

    # Add some extra indentation on the conditional continuation line.
    if (this_is_one_thing
            and that_is_another_thing):
        do_something()


结束多行结构的小括号/中括号/大括号，可以选择和上一行第一个非空字符对齐::

    my_list = [
        1, 2, 3,
        4, 5, 6,
        ]
    result = some_function_that_takes_arguments(
        'a', 'b', 'c',
        'd', 'e', 'f',
        )


或者和开始结构体的那一行代码的第一个非空字符对齐::

    my_list = [
        1, 2, 3,
        4, 5, 6,
    ]
    result = some_function_that_takes_arguments(
        'a', 'b', 'c',
        'd', 'e', 'f',
    )


----------------------
制表符还是空格符
----------------------

优先使用空格表示缩进。

只有对于已经用制表符表示缩进的历史代码，才能使用制表符表示缩进。

Python3 不允许混用制表符和空格表示缩进。

Python2 混用制表符和空格表示缩进的代码，应该转成只用空格表示缩进的代码。

启动 python2 时带上 -t 参数， python2 会对混用制表符和空格表示缩进的代码发出警告；带上 -tt 参数，这些警告会变成错误。 建议使用这些参数启动 Python2 。


------------
行长度限制
------------

每行最多包含 79 个字符。

对于没有多少结构限制的文本（比如 docstring 或者评论）， 每一行最多 72 个字符。

(?? 这一段我没有翻译，感觉也没有用??)

有些团队（比如 Pycharm） 强烈建议使用更长的代码行。对于只有一个团队维护的代码， 只要这个团队对于行长度限制达成一致即可。在确保每行 docstring 最多 72 个字符的情况下，可以把行长度限制提高到 100 个字符（Pycharm 默认行长度限制是 120 个字符）。

Python 标准库保守地限制每行代码最多 79 个字符（doctring/comment 每行最多 72 个字符）。

推荐的把长代码拆成多行代码的方法是使用括号，中括号和大括号。括号中的多行代码会被（编译器）拼接到一起（在编译器看就是一行代码）。使用这种方式比使用 \ 要好。

有时候使用 \ 把一行长代码拆成多行代码是合适的。比如对于 with 语句， 只能用 \ 拆代码::

    with open("/path/to/some/file/you/want/to/read') as file_1, \
         open("/path/to/some/file/you/want/to/written', 'w') as file_2:
        file_2.write(file_1.read())


在 assert 语句中，也只能用 /\ 拆代码。

对于连续代码，一定要合理缩进。

-------------------------------------------
代码行应该在二元操作符之前还是之后拆分
-------------------------------------------

几十年来， 推荐做法都是在二元操作符之后拆分代码行。 但是这样做有损代码可读性。首先二元操作符的排布会不整齐， 然后操作符和操作数会分不同的行。 这给代码阅读者的眼睛增加了额外的工作负担。

No::

    # No: operators sit far away from their operands
    income = (gross_wages +
              taxable_interest +
              (dividends - qualified_dividends) -
              ira_deduction -
              student_loan_interest)

为了解决可读性的问题， 数学家和他们出的书采用了相反的规范。 Donald Knuth

采用数学家的做法往往能提高代码的可读性::

    # Yes: easy to match operators with operands
    income = (gross_wages
              + taxable_interest
              + (dividends - qualified_dividends)
              - ira_deduction
              - student_loan_interest)

Python 代码中，在二元操作符之前还是之后拆分代码都可以， 只要保证统一采用一种方式即可。 如果不是历史代码， 建议采用 Knuth 的规范。



----
空行
----

顶层函数和类定义之间隔两个空行。

方法定义之间隔一个空行。

保守地使用多个空行隔开不同的函数群。 如果相关的函数都只有一行，相关函数之间可以省略空行。

在函数中，保守地使用空行分开不同的逻辑区。

（？？没有翻译，感觉不重要？？）


-----------
源码编码
-----------

python 源码请使用 UTF-8 编码（python2 中可以使用 ASCII 编码）。

文件采用 ASCII(Python2) 或者 UTF-8（Python 3）不应该有编码声明。（我不同意，好多代码都有编码声明， 当然也有很多不加编码声明）

在标准库中， 非默认编码只会出现在测试中或者是注释或者 docstring 中的包含 non-ASCII 字符的人名中。 其他情况下， 在字符串字面量中使用 \x, \u, \U, \N 转义 non-ASCII 字符串。


对于 Python 3.0 以及之后的版本， PEP 3131 规定： 所有 Python 标准库中的标识符都必须使用 ASCII-only 标识符， 只要可使用英文就使用英文（可能会有些英文缩写，专业术语不是英文）。只有在测试用例和人名中可以使用 Non-ASCII 字符。非拉丁语系的人名要给出英文译名。

鼓励面向全球的开源工程采用相似的规则。


------------
Imports
------------


引用一个包应独占一行。

Yes::

    import os
    import yss


No::

    import os, sys


从一个包中应用多个字模块是允许的::

    from subprocess import Popen, PIPE

imports 要放在文件的顶部， 在模块注释和 docstring 之后， 模块全局变量和常量之前。

imports 应该按照如下顺序分组：

    #. 标准库引用。
    #. 相关第三方包引用。
    #. 本应用/库 包引用。

组之间用空行隔开。

使用绝对路径引用包是推荐的做法， 因为这样写可读性更高同时当引包系统出问题时更容易发现问题::

    import mypkg.sibling
    from mypkg import sibling
    from mypkg.sibling import example

不过，也可以显示地使用相对路径引用包， 特别是处理复杂的包结构使得引用绝对路径引用包会非常繁琐时::

    from . import sibling
    from .sibling import example

标准库避免使用复杂的包结构，全都使用绝对路径来引包。

从包含类的模块中引用类，可以这样写::

    from myclass import MyClass
    from foo.bar.yourclass import YourClass

如果出现变量名冲突，可以这样写::

    import myclass
    import foo.bar.yourclass

然后使用 `myclass.MyClass` 和 `foo.bar.yourclass.YourClass`.

精灵不要使用通配符引用（ from <module> import * ）， 因为通配符引用会让读者和自动化工具搞不清楚都引用了哪些名称。 只有在把内部的接口暴露为外部公开 API 时，应当使用通配符引用。

用这种方式发布名称时， 请遵守下面要说的公开和内部接口的规范。


----------------------
模块级左右双下划线名称
----------------------

模块级 `dunders` （就是左右两边都有两个下滑线的名称） 比如 __name__, __author___, __version__ 等等， 应当出现在模块 docstring 之后， 除了 from __future__ 之外的任何 import 之前。 Python 要求 future 引用必须位于除了模块 docstring 之外的任何代码之前。

比如::

    """This is the example module.

    This module does stuff.
    """

    from __future__ import barry_as_FLUFL

    __all__ = ['a', 'b', 'c']
    __version__ = '0.1'
    __author__ = 'Cardinal Biggles'

    import os
    import sys

-----------
字符串引号
-----------

在 Python 中， 单引号和双引号是一样的。 PEP 并没有推荐说要使用哪个。 只要保持一致性即可。 当一个字符串中包含了单引号或者双引号时，使用双引号或单引号（避免使用转义字符能提高可读性）。

使用 三个引号 包裹的字符串时， PEP 257 要求使用双引号。


--------------------------------------------------------------------------
语句和表达式中的空格
--------------------------------------------------------------------------


如下情形下，不要使用多余的空格。


    Yes::

        spam(ham[1], {eggs: 2})

    No::

        spam( ham[ 1 ], { egss: 2 })

    在结尾逗号和括号右半边之间

    Yes::

        foo = (0,)

    No::

        bar = (0, )


    逗号，分号和冒号前

    Yes::

        if x == 4: print x, y = y, x

    No::

        if x == 4 : print x , y ; x , y = y , x


    不过冒号作为切片表达式中的二元操作符使用时， 需要在冒号两边各空一格（ 把冒号看成是最小优先级的二元操作符 ）。
    不过，在切片中， 冒号像是二元操作符， 应当在冒号两边保留对称的几个空格（可能是0个）。 在 extended slice （slice 中包括:: 号称为 extended slice）， :: 号左右两边应该有对称的几个空格（可能是0个）。如果 : 号有一边的参数为空， 空格可以省去空格。

    Yes::

        ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]
        ham[lower:upper], ham[lower:upper:], ham[lower::step]
        ham[lower+offset : upper+offset]
        ham[: upper_fn(x) : step_fn(x)], ham[:: step_fn(x)]
        ham[lower + offset, upper + offset]

    No::

        ham[lower + offset:upper + offset]
        ham[1: 9], ham[1 :9], ham[1:9 :3]
        ham[lower : : upper]
        ham[ : upper]



    函数调用的左括号之前不要留空格。

    Yes::

        spam(1)

    No::

        spam (1)


    按下标取值或者切片的左半边括号之前不要留空格。

    Yes::

        dct['key'] = lst[index]

    No::

        dct ['key'] = lst [index]


    不要为了对齐而在赋值运算符（ = ）左边（或者右边） 添加超过 1 个的空格。

    Yes::

        x = 1
        y = 2
        long_variable = 3

    No::

        x             = 1
        y             = 2
        long_variable = 3


---------------
其他推荐
---------------

在任何地方都不要以空格结束本行代码， 因为行末的空格不可见， 这可能会闹出问题： 比如反斜杠（连字符） 如果后面接空白字符就不再能够当连字符使用。 很多编辑器不允许以空格作为行结束符。

总是在下面这些二元运算符的左右两边留一个空格： =, +=, -=, ==, >, <, <>, <=, >=, in, not in, is, is not, and, or, not.

在表达式中使用不同优先级的运算符， 在优先级最低的运算符的左右两边各留一个空格。 不要使用多个空格， 左右两边的空格数要一致。

Yes::

    i = i + 1
    submitted += 1
    x = x*2 - 1
    hypot2 = x*x + y*y
    c = (a+b) * (a-b)


No::

    i=i+1
    submitted +=1
    x = x * 2 - 1
    hypot2 = x * x + y * y
    c = (a + b) * (a - b)

= 号用于表示关键字参数默认值时，请不要在 = 号左右留空格。

Yes::

    def complex(real, imag=0.0):
        return magic(r=real, i=imag)


No::

    def complex(real, imag = 0.0):
        return magic(r = real, i = imag)

函数注解中 : 之后空一格， -> 左右各空一格。

Yes::

    def munge(input: AnyStr): ...
    def munge() -> AnyStr: ...

No::

    def munge(input:AnyStr): ...
    def munge()->PosInt: ...


如果注解中有默认值，那么在 = 号左右各留一个空格。

Yes::

    def munge(sep: AnyStr = None): ...
    def munge(input: AnyStr, sep: AnyStr = None, limit=1000): ...

No::

    def munge(sep: AnyStr=None): ...
    def munge(input: AnyStr, limit = 1000): ...


不鼓励使用复合表达式（多个表达式在一行）

Yes::

    if foo == 'blah':
        do_blah_thing()
    do_one()
    do_two()
    do_three()

Rather not::

    if foo == 'blah': do_blah_thing()
    do_one(); do_two(); do_three()


有时候会把循环体（if 体）很小的 if/for/while 语句写到一行中。 对于有多个子句的表达式不要这么做（不要写到一行中）。

Yes::

    if foo == 'blah': do_blah_thing()
    for x in lst: total += x
    while t < 10: t = delay()

Definitely not::

    if foo = 'blah': do_blah_thing()
    else: do_non_blah_thing()

    try: something()
    finally: cleanup()

    do_one(); do_two(); do_three(long, argument,
                                 list, like, this)

    if foo == 'blah': one(); two(); three()


----------------------------
逗号行结束符怎么用
----------------------------

逗号行结束符通常是可有可无的。 只有在把一个元素整成一个 tuple 时， 逗号行结束符是必须的。 为了表述清晰， 推荐使用括号包裹逗号行结束符。

Yes::

    FILES = ('setup.cfg',)

Ok, but confusing:

    FILES = 'setup.cfg',

用版本控制系统（比如 git） 管理时， 在一列可能将来还会扩展的值，参数或者引入名称之后添加多余的逗号行结束符是有益的。
应该把每一个量单独放在一行， 每个量后面都都加逗号行结束符， 然后另起一行写大括号/中括号/小括号的右半边。 不过， 如果参数和括号右半边在同一行，就不要在最后一个参数后面添加逗号（tuple 中只有一个值是个例外）。


Yes:
.. code-block:: python

    FILES = [
            'setup.py',
            'tox.ini',
        ]

    initialize(FILES,
               error=True,
               )

No:
.. code-block:: python

    FILES = ['setup.cfg', 'tox.ini',]
    initialize(FILES, error=True,)


------------
注释
------------


与代码相矛盾的注释不如没有。 当修改文档时， 一定要及时更新注释。

注释应当是完整的句子。 如果一个注释是一个词组或者一句话， 首字母应当大写， 除非收个单词是代码中的以小写字母开头的标识符。（一定不要更改标识符的大小写）。

如果注释非常短， 那么注释后面的句号可以省略。 块注释通常包含了一个或者多个由完整句子构成的段落， 每个句子都应当以句号结束。

在句号后面空两格。

用英语写注释时， 遵守 Strunk and White （写作规范）。

对于非英文母语国家的 Python 程序员： 只要你不是百分之一百二地确定代码一定不会由说其他语言的人读， 请用英文写注释。


^^^^^^^^^^^^^^^^^
块注释
^^^^^^^^^^^^^^^^^

块注释注释在它们之后的一些或者全部代码。 块注释要和它们注释的代码保持相同的缩进。 块注释的每一行都以 # 加空格 开头（除非注释本身有缩进的要求， 比如 restructure text 可能有缩进的要求）。

块注释的不同段落由以单个 # 开头的空行 隔开。

^^^^^^^^^^^^^^^^^^^
行内注释
^^^^^^^^^^^^^^^^^^^

节约地使用行内注释。

行内注释指的是与被注释代码在同一行的注释。 行内注释和代码之间至少空两格。行内注释以 # 加单个空格开头。

如果行内注释的代码含义很明显， 就不必写行内注释了。


不需要这样写:

.. code-block::

    x = x + 1                            # Increment x


但是下面这样写是有帮助的:

.. code-block::

    x = x + 1                            # compensate for border


---------------------
文档字符串
---------------------

PEP 257 给出了文档字符串的写作规范。

为所有公共模块， 函数， 类和方法写文档字符串。 不必为非公用方法写文档字符串， 但是应当有注释描述方法做了什么， 这个注释出现在 def 行后面。

PEP 257 给出了文档字符串的写作规范。其中最重要的一点， 结束多行文档字符串的 """ 应该独占一行， 比如：

.. code-block:: python

    """Return a foobang

    Optional plotz says to frobnicate the bizbaz first.
    """

对于只有一行的文档字符串， 结束文档字符串的 """ 不要另起一行。



--------------------
命名规范
--------------------

Python 库遵守的命名规范有点乱， 所以我们没法给出统一的规范。 不过， 有些当下推荐的命名标准。 新的模块和包（包括第三方框架）应该遵守这些命名标准， 但是可能会有已有的包遵循不一样的命名风格， 内部一致性更重要，对这样的包做开发，请遵守这些包遵守的命名风格。


^^^^^^^^^^^^^^^^^
重写规定
^^^^^^^^^^^^^^^^^

对用户开放的公有 API 的名称应当能反映 API 的用途而不是 API 的实现。

^^^^^^^^^^^^^^^^^^^^^^^
叙述性: 命名风格
^^^^^^^^^^^^^^^^^^^^^^^

有多种不同的命名风格。 一眼就能分辨出命名风格写出可读性高的代码是有帮助的。

下列是几种有名的命名风格：


.. code-block::

    b (single lowercase letter)
    B (single uppercase letter)
    lowercase
    lower_case_with_underscores
    UPPERCASE
    UPPER_CASE_WITH_UNDERSCORES
    CapitalizedWords(or CapWords, CamelCase, StudlyCaps)
    mixedCase(differs from CapitalizedWords by initial lowercase character!)
    Capitalized_Words_With_Underscores(ugly!)


注意：在 CapWords 命名风格中，如果使用缩写， 那么缩写的每个字母都要大写。 比如 `HTTPServerError` 比 `HttpServerError` 要好。

有种命名风格给相关一组名称添加相同的短小而特殊的前缀。 这种命名风格在 Python 中用的不多， 这里只是为了完整提一下。 比如， *os.stat()* 函数返回
*st_mode*, *st_size*, *st_mtime* 等等名称组成的元组。（这么做是为了帮助熟悉 POSIX 系统调用的程序员理解变量的含义）。

X11 库中的每个公开函数的函数名都以 X 开头。 在 Pyhton 中， 这种命名风格基本上不会用， 因为属性和方法名称前已经有了对象， 函数名之前已经有了模块名。


使用下划线开头或者结尾的风格在 Python 中也很常见（这种风格可以和大小写相关的风格混合在一起使用）

    `_single_leading_underscore`: 只限内部使用的标志。 比如， `from M import *` 不会引入以下划线开头命名的对象。

    `single_trailing_underscore_`: 通常是为了避免名称冲突。 比如：

    .. code-block::

        Tkinter.TopLevel(master, class_='ClassName')

    `__double_leading_underscore`: 用于命名类中的属性时， 会引起名称改写（在 FooBar 类中， __boo 会改成 _FooBar__boo）。

    `__double_leading_and_trailing_underscore__`: 用户名称空间中神奇的对象或者属性， 比如 `__init__`, `__import__` 或者 `__file__` 。 不要自己创造这样的名称， 只使用文档中的这样的名称。


------------------
约定： 命名规范
------------------


^^^^^^^^^^^^^^^
避免使用的名称
^^^^^^^^^^^^^^^

不要用单字母 l, O, I 作为名称。

因为这几个字母太容易混淆。


^^^^^^^^^^^^^^^^^^^
ASCII 兼容性
^^^^^^^^^^^^^^^^^^^

Python 标准库中的标识符都必须是 ASCII 兼容的。


^^^^^^^^^^^^^^^^^^^^^
包和模块名
^^^^^^^^^^^^^^^^^^^^^

模块名必须简短，所有字母全小写。 下划线可以用在模块名中，只要这样写可以提高可读性。 包名也必须简单，全小写字母， 不过包名不建议使用下划线。

C extension 模块名（一般有相应的 Python 模块提供更高层次的接口）， C/C++ 模块名是 下划线 + Python 模块名。


^^^^^^^^^^^^^^^^^^^^
类名
^^^^^^^^^^^^^^^^^^^^

类名使用 CapWords 风格。

如果类的文档声明类主要作为 callable 来调用， 那么类名可以使用函数命名的规范。

内建名称自有一套规范： 除了异常名和常量采用 CapWords 命名规范外， 内建类名基本是小写的一个单词或者两个单词。


^^^^^^^^^^^^^^^^^^^^^
类型变量名
^^^^^^^^^^^^^^^^^^^^^

PEP 484 引入了类型变量， 类型变量名通常使用 CapWords 的命名风格： T, AnyStr, Num 。 推荐添加 `_co` 和 `_contra` 声明类型变量是共变的，还是反共变的。

.. code-block:: Python

    from typing import TypeVar

    VT_co = TypeVar('VT_co', covariant=True)
    KT_contra = TypeVar('KT_contra', contravariant=True)



^^^^^^^^^^^^^^^^^^^^^^^^
异常名
^^^^^^^^^^^^^^^^^^^^^^^^

因为异常是类， 所以异常命名遵守类命名的规范。 不过，需要使用 Error 后缀命名异常（如果类确实是个错误的话）。


^^^^^^^^^^^^^^^^^^^^^^^^
全局变量名
^^^^^^^^^^^^^^^^^^^^^^^^

(假设这些变量只在同一个模块内使用)。 使用和命名函数一样的命名规范。

如果模块将来会使用 `from M import *` 引用， 那么请使用 `__all__` 机制来控制暴露哪些变量；或者可以使用在全局变量名之前加下划线的方式，避免把该全局变量暴露给外部。

^^^^^^^^^^^^^^^^^^^^^^^^^
函数名
^^^^^^^^^^^^^^^^^^^^^^^^^

构成函数名的单词应该全小写，使用下划线连接。

为了保持后向兼容性时，才会使用 mixedCase 风格命名。比如 threading.py （我在 threading.py 文件中，并没有找到以 mixedCase 风格命名的函数名）。

^^^^^^^^^^^^^^^^^^^^^^^^
函数和方法的参数
^^^^^^^^^^^^^^^^^^^^^^^^

实例方法的第一个参数一定用 self 。

类方法的第一个参数一定用 cls 。

如果函数参数名和一个保留字冲突， 通常的做法是在原来的名称后面添加下划线。这样做，比使用缩写或者 spelling corruption 要好。比如 `class_` 比 `clss` 要好。（当然也可以采用同义词命名）


^^^^^^^^^^^^^^^^^^^^^^^^^^
方法名和实例变量
^^^^^^^^^^^^^^^^^^^^^^^^^^

使用函数命名的规范。构成方法和实例变量名的单词全小写， 用下划线连接。

非公开实例变量名以下划线开头。

为避免和子类发生名称冲突， 启用名称改写机制， 使用双下划线开头。

Python 使用类名改写： 如果类 Foo 存在名为 __a 的属性， Foo.__a 没法访问 __a 。 （一个钻牛角尖的程序员可以使用 Foo._Foo__a 访问 __a）。
双下划线开头的名称能避免和子类发生名称冲突， 通常用在要被继承的类中。

注意： 使用 __names 有争议（见下文）。


^^^^^^^^^^^^^^^^^^^
常量
^^^^^^^^^^^^^^^^^^^

常量一般定义在模块级别。构成模块的单词全大写，且用下划线连接。比如 *MAX_OVERFLOW* 和 *TOTAL* 。


^^^^^^^^^^^^^^^^^^
设计继承
^^^^^^^^^^^^^^^^^^

考虑并确定类的方法和实例变量（统称 attributes）应该是公开的还是不公开的。 如果疑惑， 就不公开。因为把一个公开的改成非公开很费劲。

公开 attributes 就是那些你预期让其他用户使用的的 attributes， 你必须保证公开 attributes 的后向兼容性。 非公开 attributes 是那些不准备让第三方用户使用的 attributes，不必保证非公开 attributes 的后向兼容性，它们将来可能会被修改甚至删除。

我们不使用 private 这个词，因为在 Python 中没有 attributes 是真正 private 的。

另一类 API 是 subclass API （其他语言中，常常称为 protected）。有的类是为了要被继承而写的， 不管是要扩展还是要修改类的行为。 当定义一个这样的类时， 仔细决定哪些 attributes 应该是公开的， 哪些应该是 subclass API， 那些应该只在该基类中使用。


下面是些建议，能使你的代码更加的 Python 风：

    公开的 attributes 不要以下划线开头

    如果你的公开 attributes 的名字和保留字同名， 那么可以在你的 attribute 名后面添加一个下划线。 这种做法比缩写和 corrupted spelling 要好。（尽管有这条规则， 不论何时如果变量表示一个类，变量都应该使用 cls 命名， 特别的， 类方法第一个参数必须以 cls 命名）。

    注意1： 看类方法第一个参数的命名规范。

    对于简单的 attributes, 不必添加 accessor/mutator 方法。 当你发现简单 attribute 需要有些功能行为时， Python 提供了方便的方法去扩展。比如，可以使用 property 给访问 attribute 添加隐藏的功能。

    注意1： properties 只在新式类中有用。

    注意2: 尽量减少隐藏功能的副作用。虽然有的副作用比如缓存总体来说是好的。

    注意3： 不要使用 property 实现计算复杂度高的操作， 用户都认为访问 attribute 是个低成本操作。


    如果你定义的 attributes 不想让子类用， 那么 attribute 名应该以双下划线开头，且不以下划线结尾。 这样能启动 Python 的名称改写机制。

    注意1： 名称改写只用到类名和 attribute 名，所以如果子类和父类同名， attribute 名也相同，那么还是会发生名称冲突。

    注意2： 名称改写使得某些应用（比如调试和 `__getattr__()`）变得不方便。 不过名称改写很简单，很容易手动实现。

    注意3： 不是所有人都喜欢名称改写。 综合考虑避免名称冲突的需求和方便使用的需求。

^^^^^^^^^^^^^^^^^^^^
公开和内部接口
^^^^^^^^^^^^^^^^^^^^

只有公开接口需要保证后向兼容性。 相应的， 公开接口和内部接口的写法应该明确的区分开。

有文档字符串的接口是公开的接口， 除非文档字符串明确声明它们是内部接口，不保证后向兼容性。所有没有文档字符串的接口都应当是内部接口。

为了更好的支持内省， 模块应该在 `__all__` attribute 中明确列出公开 API。 `__all__` 取值为空链表就是说模块没有公开 API。

即使正确设置了 `__all__`， 内部接口仍然应当以单下划线开头。

接口是内部的，如果包含它的接口是内部的。

被引入的名称应当被当成实现细节。 只有当有文档字符串声明它们是模块 API 时（比如 os.path 或者包中的 __init__ 常常把引用的子模块
中的名称声明为公开名称）， 它们才能被第三方用户访问。


========================
编程建议
========================


代码应该在所有 Python 实现（PyPy, Jython, IronPython, Cython, Psyco 等等）上都能正常运行。

比如， 不要指望 Cpython 的本地字符串连接实现提供效率，就是用  `a += b` 或者 `a = a + b` 表达式。 这种优化就算在 CPython 上都非常脆弱（只对有些类型有效），而且
在不使用引用计数的 Python 实现上没有效果。 实现注重效率的类库时， `''.join()` 的表述是应该优先使用的。 这能保证， 不管在 Python 的哪种实现上， 连接字符串的时间复杂度都是线性的。

与单例（比如 None） 做比较， 总是应当使用 `is` 或者 `is not` ， 不要使用 `==`。

小心， 如果你要判断一个变量是不是 None, 比如要检验一个默认取值为 None 的变量或者参数被赋值为其他值时， 不要使用 `if x`， 因为其他值也可能是 falsy （找不到比 falsy 更合适的词）的。

使用 `is not` 而不要使用 `not ... is` 。 虽然两种表述功能上相同， 但是前一种表述可读性更好。

Yes:

.. code-block::

    if foo is not None:

No:

.. code-block::

    if not foo is None:


要实现可以各种比较大小的排序操作时， 最好是实现所有 6 个比较操作（`__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`）， 而不是依赖其他代码的默认实现而只实现一种比较操作。

为了减小工作量， 可以使用 `functools.total_ordering()` 装饰器自动产生没有实现的比较操作。

PEP 207 表明 Python 在比较大小时默认满足自反性。 就是说 Python 解释器可能会把 y > x 语句换成 x < y 语句， y >= x 语句换成 x <= y 语句， 以及 x == y 换成 x != y。 `sort()` 和 `min()`
操作保证使用 < 操作， 而 max() 函数保证使用 > 操作。 不过， 为了避免出现问题，最好还是实现所有的比较操作。

不要把 lambda 表达式赋值给变量。定义函数应该使用 def 语句， lambda 表达式只用来写匿名函数。

Yes:

.. code-block::

    def f(x): return 2*x

No:

.. code-block::

    f = lambda x: 2*x

第一种表述生成的函数对象的 name 属性取值为 f, 而不是像第二种表述那样取值为 'lambda'。 这使得函数的 `%d` 更有意义， traceback 信息更有意义。把 lambda 表达式赋值给变量
让 lambda 表达式失去了它唯一的好处（那就是能嵌入到一个更大的表达式）。


自定义异常要继承自 `Exception` 而不是 `BaseException`。捕获直接从 `BaseException` 继承的异常几乎总是错的。

设计异常的层次时，更应该考虑异常是怎样被捕获的，而不是说异常是如何抛出的。有条理地回答什么出错了， 而不是仅仅声明出错了。（看 PEP 3151 看了实际的例子）

命名异常和命名类采用相同的规范。 如果异常是错误，那么异常名需要以 `Error` 做后缀。 非错误异常常被当做信号用于非本地工作流控制等场景中。 非错误异常不需要特殊的后缀。


合理使用异常链。 在 Python 3 中， `raise X from Y` 被用来明确指明用 X 异常替换 Y 异常，同时又不丢失 Y 异常的 traceback。

要故意替换一个 inner 异常时（在 Python 2 中使用 "raise X"， 在 Python 3 中使用 "raise X from None" ），确保相关细节已经传给了新的异常（比如把 KeyError 的属性名传给 ValueError， 或者把原来的异常的消息传给新异常。）

在 Python2 中抛异常， 使用 `raise ValueError('message')` ，不要用过去的 `raise ValueError, 'message'` 。

后面那种表述，不符合 Python 3 的语法。

前面那种表述同时意味着， 当异常的参数太长或者包括格式化字符串时， 因为括号的存在， 你不需要使用连字符。

捕获异常时，尽量指明要捕获的异常，而不要单单写 `except: clause`

比如， 使用:

.. code-block::

    try:
        import platform_specific_module
    except ImportError:
        platform_specific_module = None

单单使用 `except: clause` 将会捕获 `SystemExitError` 和 `KeyboardInterrupt` 异常， 这使得没法用 Control-C 中断程序， 同时也会导致一些问题。
如果想要捕获所有程序本身的错误，使用 `except Exception:`（单单使用 `except` 相当于使用 `except BaseException:`）


只有在下面两种情形下会单单使用 `except`:

#. 程序作者知道程序有错， 仅仅是为了打印出错误。
#. 代码仅仅做些扫尾工作， 待会还会使用 `raise` 把异常抛出来。在这种情况下，使用 `try ... finally` 是更好的表述。

要给异常绑定名称， 优先使用 Python 2.6 中引入的显式名称绑定语法。

.. code-block::

    try:
        process_data()
    except Exception as exc:
        raise DataProcessingFailedError(str(exc))


Python3 只支持这一种给异常绑定名称的语法。 Python2 之前的使用逗号给异常绑定名称的语法会导致语义不明的问题，不要使用。

要捕获操作系统异常时，使用 Python 3.3 引入的显式的异常层次，不要使用 errno 变量。

还有一点， 对于所有的 try/except 语句， try 子句中的代码要竟可能少， 以免太多的代码把 bug 隐藏了起来（不好调试）。

Yes:

.. code-block::

    try:
        value = collection[key]
    except KeyError:
        return key_not_found(key)
    else:
        return handle_value(value)

No:

.. code-block::

    try:
        # Too broad!
        return handle_value(collection[key])
    except KeyError:
        # will also catch KeyError raised by handle_value()
        return key_not_found(key)

一份资源尽在局部代码段中使用时， 请使用 `with` 保证资源在使用之后立即且可靠的做了扫尾工作。使用 `try/finally` 也可以。

上下文管理器应该通过独立的函数或者方法调用，只要它们做了获取和释放资源之外的操作。比如：

Yes:

.. code-block::

    with conn.begin_transaction():
        do_stuff_in_transaction(conn)

No:

.. code-block::

    with conn:
        do_stuff_in_transaction(conn)


后一种表述没有暗示 `__enter__` 和 `__exit__` 在做完事务时， 除了关闭连接还做了额外的操作。 Being explicit is Important in this case.

`return` 语句要保持一致。要不所有 `return` 语句都返回表达式，要不都不返回表达式。 如果一个 `return` 语句返回表达式，那么对于什么也不返回的 `return` 语句，应当使用 `return None` 表述，而且
函数的最后一句应该显示的 `return`。

Yes:

.. code-block::

    def foo(x):
        if x >= 0:
            return math.sqrt(x)
        else:
            return None

    def bar(x):
        if x < 0：
            return None
        return math.sqrt(x)

No:

.. code-block::

    def foo(x):
        if x >= 0:
            return math.sqrt(x)

    def bar(x):
        if x < 0:
            return
        return math.sqrt(x)

使用字符串方法而不是字符串模块

字符串方法总是比 unicode strings 提供的 API 快很多，除非是要与 Python 2.0 之前的Python 后向兼容，否则不要使用 string 模块。（我从来不使用，也不会使用）

使用 `''.startswith()` 和 `''.endswith()` 检查前缀后缀，不要使用字符串切片去检查前缀或后缀。

`startswith()` 和 `endswith()` 表意更明确更不容易发生错误。比如：

Yes:

.. code-block::

    if foo.startswith('bar'):


No:

.. code-block::

    if foo[:3] == 'bar':

比较对象的类型，请使用 `isinstance()` ， 不要直接比较类型。

Yes:

.. code-block::

    if isinstance(obj, int):


No:

.. code-block::

    if type(obj) is type(1):


判断一个对象是不是字符串时， 记住在 Python2 中， unicode sting 和 str 都是字符串。 unicode string 和 str 有相同的基类： `basestring` 。所以你可以这样判断：

.. code-block::

    if isinstance(obj, basestring)


在 Python3 中， unicode 和 basestring 不再存在。 字节组对象不再是 string(而是一列整数)。

对于序列（字符串，列表，元组）， 空序列是 falsy 的：

Yes:

.. code-block::

    if not seq:
    if seq:

No:

.. code-block::

    if len(seq):
    if not len(seq):


不要写以空格结尾的字符串字面量。这样的空格让人混淆，甚至有的编辑器会直接删除这样的空格。

布尔值和 `True/False` 做比较时，不要使用 `==`:

Yes:

.. code-block::

    if greeting:

No:

.. code-block::

    if greeting = True:


Worse:

.. code-block::

    if greeting is True:


----------------
函数注解
----------------


采纳 PEP 484 以来， 函数注解的规范一直在变。

    为保证前向兼容， Python3 代码中的函数注解应当采用 PEP 484 规定的注解语法。

    PEP 848 之前推荐的注解的试行规范现在已经不再推荐使用了。

    不过，在 Python 标准库之外，推荐尝试 PEP 484 代码规范。 比如， 为第三方库或者应用添上类型注解， 看看添加注解是不是很容易， 有没有提高代码的可读性。

    Python 标准库保存地使用注解，新代码已经重大的重构允许使用注解。

    对于要另有他用的函数注解，建议在 Python 文件顶部添加如下面所示的注释：

    .. code-block::

        # type: ignore

    这个注释告诉 type checker 忽略所有注解。（更精细的取消 type checker 报警的方法参见 PEP 484）

    和 Linter 一样， type checker 是可选的， 独立的工具。Python 解释器默认不会做类型检查，函数注解默认不能改变代码的行为。

    用户可以选择使不使用 type checker 。不过，希望第三方包的使用者可以使用 type checker 对第三方包做检查。为此， PEP 848 推荐
    使用 `stub` 文件： `.pyi` 文件， type checker 会优先读取 .pyi 文件。`stub` 文件可以通过类库发布，也可以通过 typeshed repo 发布。

    需要保证后向兼容性的代码， 可以把类型注解写到注释中。请查看 PEP 848 中的相关章节。








