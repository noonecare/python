===============
Mock or Docker
===============

:作者: 王蒙
:标签: test, mock, fake, monkeypatch, test environment, resource, unit test, 单元测试

:简介:

    Mock 和 Docker 的方式都为测试提供执行环境。该选择哪个？

.. contents::

目标读者
========

Python 开发

预备知识
=============

pytest, docker, monkeypatch

问题
=======

- 如何使用 Docker 提供测试环境
- 如何 mock 环境和资源
- 哪种方式更好


解决办法
========

如何使用 Docker 提供测试环境？

    如果测试需要 Elasticsearch 数据库服务，那么先去 `Docker.hub`_ 上找到 Elasticsearch 镜像，找到该镜像的说明文档，按照说明文档在本地启动 Elasticsearch 服务，然后做测试。

    整个过程非常简单，只要懂的如何使用 Docker ，整个过程没有任何难度。


如何 mock 环境和资源？

    工具：
        - `unittest.mock`_ 和 unittest.patch： 伪造类函数等。
        - `pytest monkeypatch`_ ： 伪造属性值，最厉害的是，这种伪造只在使用 monkeypatch 的测试用例中生效。

    说 mock 环境和资源，其实不对。更准确地说是 mock 了 Python Object （的属性）。比如使用 requests.get 访问 Elasticsearch 服务。mock 要做的不是说提供一个 Elasticsearch 服务，而是重定义 request.get 函数，使得 request.get 看起来就像是在访问 Elasticsearch。



哪种方式更好？

    使用哪种方式做测试的代码都有。但是我认为，为了测试自动化，最终的代码要使用 mock 的方式做测试（不要使用 docker）。

    我一般是这样做测试，还是举刚才的例子。我的代码要用 requests.get 访问 Elasticsearch 。那么我：

        #. 开始时，使用 Docker 做测试。
        #. 给出测试用例的输入，调试程序时，捕获 requests.get 对于每个输入的输出值（收集输出值和输出值，构造函数 f）。
        #. 调用 monkeypath 设置 reqeusts 的 get 属性值为上一步构造出的函数 f。
        #. 上一步中 f 的输出值是 `Response` 类，这个类的实例可能不容易构造。在这种情况下可以使用 `MagicMock` 类伪装出 `Response` 类的实例。
        #. 到这一步，就完成了使用 mock 的资源做测试的测试用例。从此不必再启动 Docker Elasticsearch 服务做测试（抛弃之前使用 Docker的方法），测试完全自动化。

参考文献
=========

.. _pytest monkeypatch: https://docs.pytest.org/en/latest/monkeypatch.html?highlight=patch
.. _unittest.mock: https://docs.python.org/3/library/unittest.mock-examples.html?highlight=mock
.. _Docker.hub: http://dockerhub.com/