- acceptance test(functional tests)

    把软件当做黑盒做测试，确保软件实现了当初设计的功能。这部分测试，不是由开发者做的，而是由 QA staff 甚至客户去做的。


    +---------------------------+-------------------+
    | Application Type          | Tool              |
    +===========================+===================+
    | Web Application           | Selenium          |
    +---------------------------+-------------------+
    | Web Application           | zope.testbrowser  |
    +---------------------------+-------------------+
    | WSGI application          | paste.test.fixture|
    +---------------------------+-------------------+
    | Gnome Desktop application | dogtail           |
    +---------------------------+-------------------+
    | Win32 Desktop application | pywinauto         |
    +---------------------------+-------------------+

更详细的信息，参考`python 测试工具大全`_ 。

- unit test

    针对类函数功能的测试，单元测试由开发人员来写，是 TDD 的基础。

- Functional tests

    重点测试整体的功能而不是每个代码单元。和 acceptance tests 的不同，在于 acceptance tests 完全是使用用户接口做测试。
    Functional tests 可以不必从用户接口做测试。比如测试 HTTP 服务器时，使用浏览器访问（模拟用户的使用）就是 acceptance tests。
    使用 Postman 直接整 HTTP 请求去测试，就是 Functional tests。


- Integration tests

    重点测试不同软件部件之间是否如预期的那样交互。



- Load and performance testing

    performance testing 很难，不同机器之间 CPU ，Memory 和 IO 性能不同会影响程序的性能。就算是同一台机器 CPU, Memory 和
    IO 性能也不是一层不变的。

- Code quality testing

    - PEP8 规范（pylint ）
    - Complexity metrics, 比如圈复杂度（flake8 可以测）
    - 代码覆盖率（coverage）
    - 编译时 warning 的数量（python 没有，Java 有）
    - 文档是否够全（这个我没有找到现成的工具去做，估计语意方面的检查只能靠人去检查）

.. _python 测试工具大全: https://wiki.python.org/moin/PythonTestingToolsTaxonomy


Python standard test tools
==========================

unittest, nosetest, pytest, doctest

- pytest 基本包含了其他三个包提供的功能，写法很 pythonic, 提供了丰富的 test fixtures（自定义 test fixtures 也非常方便），无疑是目前 Python 最好的 test tool。

- unittest 是 Python 内建包，不过写法过于像 Java, 丢失了 Python 简洁的优势。只有 unitest.mock 模块，我还会时不时用一下。

- nosetest github 上很久不更新了，写法上 pytest 和 nosetest 挺像的。不过我选择 pytest。

- doctest 文档中插入示例代码，doctest 会执行这些示例代码做测试。这样做可以确保及时更新文档，思路很新颖。不过 pytest 也提供了文档测试的功能，所以我就没再看 doctest。


Pytest 我已经很熟悉了，就不再赘述了。


Testing Coverage
----------------

使用 pytest 执行代码

.. code-block::

    coverage run -m pytest {module or directory you want to test, default is .}

命令行报告 coverage 信息

.. code-block::

    coverage report

html 报告 coverage 信息

.. code-block::

    coverage html


Building a fake
---------------

unittest.mock
unittest.patch
pytest monkeypatch test fixture

为测试提供自定义的（或者说模拟的）外部包行为，执行环境等。

Testing environment and dependency compatibility
------------------------------------------------

不管开发，测试还是部署，最好使用 isolation 的执行环境。常见提供 isolation 的技术有： 虚拟机（使用 vagrant 管理会很方便），Docker（部署常用），virutalenv/pyvenv 等。

最好使用 CI 流程做测试，在测试的过程中， CI 可以使用 docker/虚拟/虚拟解释器等提供的 isolation 执行环境。

jenkins 可以直接选择在什么 docker 环境中执行，非常方便。其他 CI 工具应该也能提供这样的操作。


Dependency matrix testing
-------------------------

tox 常用，如下图所示，指明每个测试环境。

.. code-block::

    [tox]
    downloadcache = {toxworkdir}/cache/

    envlist =
        ; py26 support was dropped in django1.7
        py26-django{15,16},
        ; py27 still has the widest django support
        py27-django{15,16,17,18,19},
        ; py32, py33 support was officially introduced in django1.5
        ; py32, py33 support was dropped in django1.9
        py32-django{15,16,17,18},
        py33-django{15,16,17,18},
        ; py34 support was officially introduced in django1.7
        py34-django{17,18,19},
        ; py35 support was officially introduced in django1.8
        py35-django{18,19}

    [testenv]
    usedevelop = True
    deps =
        django{15,16}:south
        django{15,16}:django-guardian<1.4.0
        django15: django==1.5.12
        django16: django==1.6.11
        django17: django==1.7.11
        django18: django==1.8.7
        django19: django==1.9
        coverage: django==1.9
        coverage: coverage==4.0.3
        coverage: coveralls==1.1

    basepython =
        py35: python3.5
        py34: python3.4
        py33: python3.3
        py32: python3.2
        py27: python2.7
        py26: python2.6

    ...


expert python programming 读 https://github.com/ClearcodeHQ/ianitor， 来学习 tox, travis 在提供测试环境方面的实践。

Travis 是在 github 中广泛使用的 CI 工具，Travis 免费为 github 项目提供服务。之后在 github 写代码，可以使用 Travis 做 CI。


Document-driven development
===========================

doctest/pytest 都提供了执行文档示例代码做测试的功能。这使得 Document-driven development 变成可能。

