==============
C extension
==============

:Author: 王蒙
:Tags: Python 开发，优化，高性能计算，C

:abstract:

    本节介绍 C extension 的原理，介绍几种写 C extension 的方式，介绍 C extension 常见的应用。

.. contents::

Audience
========

Python 开发


Problem
=========

- C extension 有什么用
- C extension 怎么写
- C extension 原理


Solution
===========

C extension 有什么用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

常见有两种应用：

    - 需要高性能，Python 满足不了。
    - 需要使用 C 链接库文件。

C extension 怎么写
~~~~~~~~~~~~~~~~~~~~~~~~

ctypes/cffi, Cython 和直接调用 Python/C API 三种写 C extension 的方式， ctypes/cffi 最简单，Cython 次之，直接调用 Python/C API 最难。一般很少直接调用 Python/C API 写 C extension，Cython 已经提供了很高的灵活性。

- ctypes/cffi

    ctypes/cffi 都能在 Python 中调用 C 链接库函数。要做的工作是：

        - 引用 C 链接库函数
        - 完成 C 函数 signature 到 Python 函数 signature 的映射

    ctypes 和 cffi 类似，都提供了 Python 数据类型到 C 数据类型的映射。

    请阅读 `ctypes_libc_printf.py`_,  `cffi_qsort.py`_,  `ctypes_qsort.py`_ 示例代码，学习使用 ctypes/cffi。

- Cython

    Cython 是编译器，是包含 Python 的一门语言，是一个Python包。

    Cython 定义参数类型。在 Cython 中不带参数类型的话，说明参数的类型是 PyObject， 带参数类型的话，Cython 会合理地把 PyObject 转成相应的 C 类型(如果不能转，会报错)。

        .. code-block:: python

            def fibonacii(unsigned int n):
                ...

    Cython cdef 修饰符。 cdef 修饰符修饰函数定义，表示该函数是 c function（不会进行 PyObject 到 C 类型的来回转换）

        .. code-block:: cython

            cdef long long fibonacci_cc(unsigned int n):
                ...

    Cython 释放 GIL。CPython 解释器要求，访问 PyObject 时必须加 GIL。如果不需要访问 PyObject 类型的数据，不需要加 GIL。我们使用 C extension 一般都不想加 GIL。释放 GIL 的代码如下：

        .. code-block:: cython

            def fibonacci(unsigned int n):
                # 释放 GIL
                with nogil:
                    result = fibonacci_cc(n)
                return result

            # 下面是另一种释放全局锁的方式，因为 fibonacci_cc 函数从来都不访问 PyObject 数据类型，所以可以用如下方式定义
            # fibonacci_cc。这样定义之后，fibonacci_cc 函数总是会释放GIL。
            cdef long long fibonacci_cc(unsigned int n) nogil:
                if n < 2:
                    return n
                else:
                    return fibonacci_cc(n - 1) + fibonacci_cc(n - 2)



    Cython 打包。下面是使用 Cython 写 extension 时，setup.py 文件的写法。具体的，cythonize(['fibonacci.pyx']) 会编译 finobacci.pyx 文件成 .c 文件，并且返回 Extension 类型的对象（ext_modules 只接受 Extension 类型的值）。
    考虑到用户装包时，可能缺少 cython 编译环境，所以常常提供多种装包方式。为了提供多种装包方式 setup.py 就会变得复杂，`setup.py`_ 提供了完善的装包方式。

        .. code-block:: python

            from setuptools import setup
            from Cython.Build import cythonize


            setup(
                name='fibonacci',
                ext_modules=cythonize(['fibonacci.pyx'])
            )



- 直接调用 Python/C API

    上面说到 Cython 能把 .py 和 .pyx 文件编译成 .c 文件。Cython 编译的结果就是直接使用 Python/C API 写的 C 源码（就是这里要讲的最后一种写 C extension 的方式）。

    `直接调用 Python/C API 写 C extension`_ ，比较麻烦。包含以下几步：

        #. 定义要用 C/C++ 实现的函数
        #. 定义刚才实现函数的 Python 接口（会调用 Python/C API 实现 C/Python 数据类型转换，引用计数的增减以及释放 GIL 等）
        #. 一堆 boiler-plate 代码，很繁琐，但是所有模块写的都差不多。主要包括，方法定义，模块定义，初始化模块。

            .. code-block:: c

                static char fibonacci_docs[] =
                    "fibonacci(n): Return nth Fibonacci sequence number "
                    "computed recursively\n";

                # 定义方法
                static PyMethodDef fibonacci_module_methods[] = {
                    {"fibonacci", (PyCFunction)fibonacci_py,
                     METH_VARARGS, fibonacci_docs},
                    {NULL, NULL, 0, NULL}
                };

                # 定义模块
                static struct PyModuleDef fibonacci_module_definition = {
                    PyModuleDef_HEAD_INIT,
                    "fibonacci",
                    "Extension module that provides fibonacci sequence function",
                    -1,
                    fibonacci_module_methods
                };

                # 初始化模块
                PyMODINIT_FUNC PyInit_fibonacci(void) {
                    Py_Initialize();
                    return PyModule_Create(&fibonacci_module_definition);
                }


        #. setup.py 文件

            .. code-block:: python

                from setuptools import setup, Extension


                setup(
                    name='fibonacci',
                    ext_modules=[
                        Extension('fibonacci', ['fibonacci.c']),
                    ]
                )

    - Python/C 类型转换 API:

        - PyArg_ParseTuple: 把 PyObject* (Python 数据类型)编译成 C 类型。
        - Py_BuildValue: 把 C 类型编译成 PyObject*(Python 数据类型)。
        - PyErr_SetString: 报错。
        - Py_BEGIN_ALLOW_THREADS;...;Py_END_ALLOW_THREADS; 释放GIL 。

    - Reference Count:

        CPython 垃圾回收： 如果变量的 reference count 为 0，那么在 gc 时，会释放该变量所占内存。

        Owning a reference： 谁需要执行 Py_DECREF

        #. pass reference, 函数 A 调用函数 B, 函数 B 的返回值的 reference 由 A 函数负责处理。（函数 A 认为返回值的 reference count 为 0， 当然常见的情况是 a = B(), 这时候返回值的 reference count 为 1）。
        #. borrow reference，变量 a 作为参数传给 f 函数，函数 f 不负责处理 a 的 reference count。大部分函数是这种方式。
        #. stolen reference，变量 a 作为参数传给 f 函数，函数 f 负责处理 a 的 reference count。PyTuple_SetItem() 和 PyList_SetItem()。

        todo: 为什么不统一都整成 borrow reference ? stolen reference 为什么要存在?

        不同版本 Python 解释器，对于循环引用的处理不同，尽量不要自定义 **\_\_del\_\_** 方法。

        直接调用 Python/C API 写 c extension 容易出现内存泄露的问题。一定要充分测试（比如多次使用该函数，如果会导致内存占用明显增加，那么说明可能有内存泄露）。



C extension 原理
~~~~~~~~~~~~~~~~~~~~~~~

C extension 的原理：

    - Python/C API 完成了 Python 数据类型（PyObject*）和 C 数据类型的转换。
    - CPython 使用 Reference Count 的方式做垃圾回收。直接调用 Python/C API 时，需要自己增减 PyObject* 的引用计数（非常容易出错）。
    - CPython 访问 PyObject* 类型数据时，必须加锁。如果不访问 PyObject* 类型的数据，几乎总是会把锁去掉。


Reference
==========

- Expert Python Programing chapter 7 Python Extensions in Other Languages


.. _ctypes_libc_printf.py: https://github.com/PacktPublishing/Expert-Python-Programming_Second-Edition/blob/master/chapter7/ctypes_libc_printf.py
.. _cffi_qsort.py: https://github.com/PacktPublishing/Expert-Python-Programming_Second-Edition/blob/master/chapter7/cffi_qsort.py
.. _ctypes_qsort.py: https://github.com/PacktPublishing/Expert-Python-Programming_Second-Edition/blob/master/chapter7/ctypes_qsort.py
.. _setup.py: https://github.com/PacktPublishing/Expert-Python-Programming_Second-Edition/blob/master/chapter7/fibonacci_cythonize_optionally/setup.py
.. _直接调用 Python/C API 写 C extension: https://github.com/PacktPublishing/Expert-Python-Programming_Second-Edition/tree/master/chapter7/fibonacci_c_releasing_gil