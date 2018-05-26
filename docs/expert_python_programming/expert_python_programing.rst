Chapter 1: Current Status of Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Where are we now and where we are going?

    * December 3, 2008 - the release date of Python 3.0
    * PEP 404 - the official document that "un-released" Python 2.8 and officially closed the 2.x branch.
    * Still some python developers prefer python2 to python3.


Why and how does Python change ?

    * Python 变化，因为有需求要 Python 变化

    * Python 应用越来越广，要解决的问题越来越多，Python 需要改变

    * 很多Python 的变化源于某个特定方面的使用，比如 Python web 开发的应用场景，促使 Python 在并发方面提高

    * 还有一些改变，是因为一些内建包写的不好，一些设计不好，需要修正。


Getting up to date with changes – PEP documents

    * Python 重要的更新都会在 PEP 文档中讨论。关注 https://www.python.org/dev/peps， 关注最新的 PEP 文档，就能跟上Python的变化。

    * Python PEP 文档中有三方面信息：

        #. Informing:
        #. Standardizing:
        #. Designing:


Python3 是未来和现在，但不能完全摒弃 Python2, 需要做 Python2 和 Python3 的兼容工作。Python2 和 Python3 的主要不同有以下三点：

    * Syntax Changes

        #. print("hello world") vs print "hell world"
        #. raise from 只在 Python3 中是有效的语法
        #. python 2 默认编码是 ascii， python3 的默认编码是 utf-8
        #. python2 中 except IOException, RuntimeException: 是有效的语法， python3 中必须加括号， except (IOException, RuntimeException):
        #. python2 中 except Exception, ex 变成了 except Exception as e
        #. <> removed in favor of !=
        #.

    * Changes in Standard library

    * Changes in datatypes and collections


The Python tools and techniques used for maintaining cross-version compatibility



应用级虚拟环境：

    * virtualenv
    * pyvenv
    * buildout
