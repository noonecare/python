Creating A Package
==================


Creating a package
------------------


Python 的打包工具比较混乱。`PyPA(Python Package Authorization)`_ 推荐使用 `setuptools` 给 Python 打包，PyPa 还提供了
`Python Packing User Guide 文档`_ 作为 Python 打包的权威指南。

我之前一直认为 Python built-in package 要比第三包好，我优先使用 Python built-in package。但事实证明，真的有些第三方要比
Python built-in package 好很多。


PyPA 推荐的包管理工具如下

    #. pip 装包
    #. setuptools 打包
    #. wine 上传包
    #. virtualenv or venv 构建项目级别的独立开发环境
    #. wheel 能打成 wheel 包尽量导成 wheel 包
    #. warehouse（据说 warehouse 对于 PyPI 有很多优势，将要取代 PyPI, 不过暂时还都是用的 PyPI）


Project Configuration
---------------------


setup.py
^^^^^^^^



setup.py 文档，代码统一更新

#. setup.py 一般会读取 README.rst 的内容，把 README.rst 作为 setup 函数中的 long_description 的值。
#. setup.py 一般会读取 project 下的 `__init__.py` 文件中的 `__VERSION__` 变量值，以这个值作为 setup 函数的 version 参数值。
#. dependencies 中写项目的依赖，有的项目会有 requirements.txt 文件（《expert python programming》建议以包发布应用，包中不建
议有 requirements.txt 文件，我也觉得 dependencies 中都有依赖，没必要在写一份儿，不过很多开源项目中有 requirements.txt 文件。
如果有 requirements.txt， 《Expert Python Programming》建议读取 requirements.txt , 把该内容写到 setup.py 的 dependencies
参数中）。


The Custom setup command
^^^^^^^^^^^^^^^^^^^^^^^^

setup.py 中的 entry_points 选项可以定义 command, 定义了 command 之后，就能打出可执行脚本。


Working with packages during development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

pip install <project-path>  装包

pip uninstall <project-path>    卸包

最有用的是

pip install -e <project-path>

python setup.py develop

是以开发模式安装包，就是当前对包的改动，可以立即反应到当前 Python 解释器环境中。


Namespace Packages
------------------

为什么要用 Namespace Packages?

Namespace Package 相当于是比 package 更高一级的抽象。如果包下面包含子包，而子包需要独立发布。这时候，你需要 Namespace Package。
只是 package 做不到的。package 只能 install 全部的子包。

《expert python programming》 原话是这么说的：

.. code-block::
    Namespace packages are especially useful if you have your application components developed, packaged, and versioned
    independently but you still want to access them from the same package.



定义 Namespace Packages

Python3 定义 Namespace Package 特简单，只有该目录下有 python 源码，且该目录下没有 `__init__.py`，那么这个目录就是个
Namespace。

Python2 定义 Namespace Package 需要在 setup.py 文件中，指明 `namespace_packages`， 而且就算是 namespace package, 该目录下也
需要有 `__init__.py` 文件。Python2 中定义 namespace package 的 setup.py 文件，大致如下：

.. code-block::

    from setuptools import setup

    setup(
        name='acme.templating',
        packages=['acme.templating'],
        # python2 必须指明 namespace_packages
        namespace_packages=['acme'],
    )


不过简单地在 setup.py 中指明 `namespace_package` 如果被人遗忘，所以在 Python2 中，最好在 namespace 下的
`__init__.py` 文件中写上

    .. code-block::

        __import__('pkg_resources').declare_namespace(__name__)


Uploading a package
-------------------

先打包，打完包后使用

# 上传到 index 中
twine upload dist/*
# 在 index 中 register
twine register dist/*


PyPI
^^^^

PyPI 是 Python 官方开源包索引。


Uploading


\.pypirc
^^^^^^^^

.. code-block::

    [distutils]
    index-server =
        pypi
        other

    [pypi]
    repository: <repository-url>
    username: <username>
    password: <password>

    [other]
    repository: <repository-url>
    username: <username>
    password: <password>


\.pypirc is supported by pip, twine, distutils, and setuptools.


Source package versus built packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

sdist
^^^^^

python setup.py sdist

bdist
^^^^^

python setup.py bdist


# 推荐的做法，打 wheel 包
python setup.py bdist_wheel



Standalone executables
----------------------


Popular Tools:

#. PyInstaller
#. cx_Freeze
#. py2exe and py2app

Security of Python code in executable packages
----------------------------------------------

最安全的方式是使用 RESTFUL 接口提供服务。


今天我用 pip 装包

.. code-block::

    $ /e/python-3.6.5/Scripts/pip install textract
    Collecting textract
      Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None))                                                                                                                                                                                                after connection broken by 'SSLError(SSLError(1, '[SSL: CERTIFICATE_VERIFY_FAIL                                                                                                                                                                                               ED] certificate verify failed (_ssl.c:833)'),)': /simple/textract/
      Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None))                                                                                                                                                                                                after connection broken by 'SSLError(SSLError(1, '[SSL: CERTIFICATE_VERIFY_FAIL                                                                                                                                                                                               ED] certificate verify failed (_ssl.c:833)'),)': /simple/textract/
      Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None))                                                                                                                                                                                                after connection broken by 'SSLError(SSLError(1, '[SSL: CERTIFICATE_VERIFY_FAIL                                                                                                                                                                                               ED] certificate verify failed (_ssl.c:833)'),)': /simple/textract/
      Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None))                                                                                                                                                                                                after connection broken by 'SSLError(SSLError(1, '[SSL: CERTIFICATE_VERIFY_FAIL                                                                                                                                                                                               ED] certificate verify failed (_ssl.c:833)'),)': /simple/textract/
      Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None))                                                                                                                                                                                                after connection broken by 'SSLError(SSLError(1, '[SSL: CERTIFICATE_VERIFY_FAIL                                                                                                                                                                                               ED] certificate verify failed (_ssl.c:833)'),)': /simple/textract/
      Could not fetch URL https://pypi.python.org/simple/textract/: There was a prob                                                                                                                                                                                               lem confirming the ssl certificate: HTTPSConnectionPool(host='pypi.org', port=44                                                                                                                                                                                               3): Max retries exceeded with url: /simple/textract/ (Caused by SSLError(SSLErro                                                                                                                                                                                               r(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:833)'),                                                                                                                                                                                               )) - skipping
      Could not find a version that satisfies the requirement textract (from version                                                                                                                                                                                               s: )
    No matching distribution found for textract

实际体会了下，什么叫做官方 PyPI 不是高可用的。我昨天用官方 PyPI 还是好好的。今天就这样了。切换成 aliyun 之后，问题解决。
这次经历印证了手中的内容，一个公司还是要有自己的 PyPI。



.. _PyPA(Python Package Authorization): https://github.com/pypa
.. _Python Packing User Guide 文档: https://packaging.python.org