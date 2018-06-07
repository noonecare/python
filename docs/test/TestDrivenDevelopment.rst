





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

