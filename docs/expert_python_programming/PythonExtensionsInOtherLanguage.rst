多种方式写 Extension。

推荐使用 CPython 写 extension。
如果只是引用链接库文件，可以使用 ctypes（built-in package） 和 cffi(third-party package) 来写。
直接使用 Python/C API 来写 extension， 对于理解 extension 的原理很重要，但是直接写，容易出错，特别是内存方面的错。


C extension:

对于 Cpython 使用 C/C++ 来写 C extension。所以 Python 中的数据，在C 语言看来都是 PyObject* 。Python/C API 需要加全局锁
GIL 才能安全的使用。不适用 Python/C API 的 C 代码，最好不要加 GIL 锁，不加锁可以利用多核。

Python/C API 中最常用的几个是 PyArg_ParseTuple, Py_BuildValue 这系列的完成 PyObject* 和 C 语言类型转换的函数。除此之外还
有加锁释放锁的语句 Py_BEGIN_ALLOW_THREADS, Py_END_ALLOW_THREADS；异常处理的 PyERR_SetString, PyExc_ValueError；处理
Reference Counting 的 Py_INCREREF, Py_DECREF 。


使用 Python/C API 直接写 C extension ，比较麻烦。包含以下几步：

    #. 定义要用 C/C++ 实现的函数
    #. 定义刚才实现函数的 Python 接口
    #. 一堆 boiler-plate 代码，很繁琐，但是所有模块写的都差不多。主要包括，方法定义，模块定义，初始化模块。

    .. code-block::

        static char fibonacci_docs[] =
            "fibonacci(n): Return nth Fibonacci sequence number "
            "computed recursively\n";


        static PyMethodDef fibonacci_module_methods[] = {
            {"fibonacci", (PyCFunction)fibonacci_py,
             METH_VARARGS, fibonacci_docs},
            {NULL, NULL, 0, NULL}
        };


        static struct PyModuleDef fibonacci_module_definition = {
            PyModuleDef_HEAD_INIT,
            "fibonacci",
            "Extension module that provides fibonacci sequence function",
            -1,
            fibonacci_module_methods
        };


        PyMODINIT_FUNC PyInit_fibonacci(void) {
            Py_Initialize();
            return PyModule_Create(&fibonacci_module_definition);
        }


    #. setup.py 文件

        .. code-block::

            from setuptools import setup, Extension


            setup(
                name='fibonacci',
                ext_modules=[
                    Extension('fibonacci', ['fibonacci.c']),
                ]
            )

内存管理， 直接用 Python/C API 写 extension 很容易发生内存泄露，一定要充分测试，模块是不是很发生内存泄露。
CPython 垃圾回收的原理是： 如果一块内存（变量）的 reference count 为了，那么在 gc 时，会释放这块内存。所有 python 中的变
量都是 PyObject* ，都是指向内存的引用。 del a 会删除 a， 相应的 a 指向的内存的 reference count 会减 1。变量a 的生命周期
结束，那么变量 a 指向的内存的 reference count 减 1。函数调用时,reference count 如何算，有三种情况。

Owning a reference： 谁需要执行 Py_DECREF

#. pass reference, 函数 A 调用函数 B, 函数 B 的返回值的 reference 由 A 函数负责处理。（函数 A 认为返回值的 reference count 为 0， 当然常见的情况是 a = B(), 这时候返回值的 reference count 为 1）。
#. borrow reference，变量 a 作为参数传给 f 函数，函数 f 不负责处理 a 的 reference count。大部分函数是这种方式。
#. stolen reference，变量 a 作为参数传给 f 函数，函数 f 负责处理 a 的 reference count。PyTuple_SetItem() 和 PyList_SetItem()。

为什么不统一都整成 borrow reference ? stolen reference 为什么要存在?

Py_REFCNT 可以得到 REFCNT。




