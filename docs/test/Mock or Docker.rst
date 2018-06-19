===============
Mock or Docker
===============

:作者: 王蒙
:标签: test, mock, fake, monkeypatch, test environment, resource, unit test, 单元测试

:简介:

    Docker 提供执行环境做测试，Mock 伪造外部环境做测试。实际做单元测试时，该选择该种方式？

.. contents::

目标读者
========

Python 开发

预备知识
=============

pytest, docker, monkeypatch, mock

问题
=======

- 如何使用 Docker 提供测试环境
- 如何 mock 环境和资源
- 哪种方式更好


解决办法
========

如何使用 Docker 提供测试环境？

    如果测试需要 Elasticsearch 数据库服务，那么先去 `Docker.hub`_ 上找到 Elasticsearch 镜像，找到该镜像的说明文档，按照说明文档在本地启动 Elasticsearch 服务，然后就可以测试（使用 Elasticsearch 服务的程序）。

    整个过程非常简单，只要懂的如何使用 Docker ，整个过程没有任何难度。


如何 mock 环境和资源？

    工具：
        - `unittest.mock`_ 和 unittest.patch： 伪造 Python Object 。
        - `pytest monkeypatch`_ ： 伪造 Python Object 的属性值，最厉害的是，这种伪造只在使用 monkeypatch 的测试用例中生效。

    修改 Python Object 的属性值，使得 Python Object 看起来就像是在使用某种特定的资源（环境）。比如使用 requests.get 访问 Elasticsearch 服务。mock 要做的不是说提供一个 Elasticsearch 服务，而是重定义 request.get 函数，使得 request.get 看起来就像是在访问 Elasticsearch。



哪种方式更好？

    使用哪种方式做测试的代码都有。但是我认为，为了测试自动化，最终的代码要使用 mock 的方式做测试（不要使用 docker）。

    我一般是这样做测试的。还是举刚才的例子，我的代码要用 requests.get 访问 Elasticsearch 。那么我：

        #. 开始时，使用 Docker 做测试。
        #. 给出测试用例的输入，调试程序时，捕获 requests.get 对于每个输入的输出（收集输入输出，构造函数 f）。
        #. 调用 monkeypath 设置 reqeusts 的 get 属性值为上一步构造出的函数 f。
        #. 上一步中 f 的输出值是 `Response` 类，这个类的实例不容易构造。在这种情况下可以使用 `MagicMock` 类伪装出 `Response` 类的实例。
        #. 到这一步，就完成了mock 资源做测试的操作。从此不必再启动 Docker Elasticsearch 服务做测试（抛弃之前使用 Docker 的方法），测试完全自动化。


    补充一句，很多 CI 工具（比如 Jenkins） `对于 Docker 提供了支持`_ 。所以如果你确信一定只会使用 CI agent 做测试，那么就算使用了 Docker，测试也是能够自动执行的。

参考文献
=========

.. _pytest monkeypatch: https://docs.pytest.org/en/latest/monkeypatch.html?highlight=patch
.. _unittest.mock: https://docs.python.org/3/library/unittest.mock-examples.html?highlight=mock
.. _Docker.hub: http://dockerhub.com/
.. _对于 Docker 提供了支持: https://jenkins.io/doc/book/pipeline/docker/