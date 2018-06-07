===============
Mock or Docker
===============

:Author: 王蒙
:Tags: test, mock, fake, monkeypatch, test environment, resource, unit test, 单元测试

:abstract:

    可以使用 Mock 的方式，也可以使用 Docker 的方式为测试提供自定义的（或者说模拟的）外部包行为，执行环境等。这一节介绍具体该怎么做。

.. contents::

Audience
========

Python 开发

Prerequisites
=============

pytest, docker

Problem
=======


- 如何 mock 环境和资源
- 如何使用 Docker 提供测试环境
- 哪种方式更好


Solution
========

如何 mock 环境和资源？

    工具：
        - `unittest.mock`_ 和 unittest.patch
        - `pytest monkeypatch`_

如何使用 Docker 提供测试环境？

    如果测试需要 postgresql 数据库服务，那么先去 Docker.hub 上找到 postgresql 镜像，找到该镜像的说明文档，按照说明文档在本地启动 postgresql 服务，然后做测试。

哪种方式更好？

    使用 mock 的方式，方便自动执行单元测试。

    使用 Docker 的方式，相当于你把第三方包（比如上面例子中，访问 postgresql 的包）也测试了下。

Reference
=========

.. _pytest monkeypatch: https://docs.pytest.org/en/latest/monkeypatch.html?highlight=patch
.. _unittest.mock: https://docs.python.org/3/library/unittest.mock-examples.html?highlight=mock