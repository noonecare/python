====================
项目文档
====================

:作者: 王蒙
:标签: 文档，python 开发，编码规范，持续集成

:简介:

    没有文档介绍的项目，别人没法使用。所以文档对于项目至关重要。

.. contents::


目标读者
========

Python 开发

预备知识
=============

问题
=======

- 技术文档写作规则
- 项目通常包含哪些文档
- Python 推荐的文档格式
- 持续集成和文档托管

解决办法
========


技术文档写作7个规则
~~~~~~~~~~~~~~~~~~~~~~~~~~


#. 开始写的时候，专注于内容；然后整个检查一遍，整理格式。
#. 每个文档针对明确的读者。
#. 文档应该写的尽可能简单。比如一句话不要太长，一个段落不要太长等等。
#. 分主题组织文档，给每篇文档写合适的题目。选择标题时，可以想，如果读者对文档内容感兴趣，他会在 Google 中输入什么。
#. 使用统一的格式，使用模板。
#. 不要写过多的文档，特别不要在文档中写废话，开玩笑等等。
#. 示例代码，选择真实的，拿来就能运行的代码片段。


通常项目要写哪些文档
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Design
- Usage
    - Recipe
    - Tutorial
    - Module Helper

- Operations

    - Installation and deployment documents
    - Administration documents
    - FAQ
    - Documents that explain how people can contribute, ask for help, or provide feedback



A reStructuredText Primer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python 文档推荐使用 reStructuredText 格式写。

- `reStructuredText Premier`_

- `Sphinx`_ 是比 Docutils 要强大的工具。

    - Sphinx 编译出的文档支持检索。
    - Sphinx 编译出的文档有多种主题可选，更美观。
    - Sphinx 支持 toctree 命令，能生成 index 页。
    - Sphinx 能根据 Python 源码的 docstring 生成 API 文档。


- Sphinx 提供的重要的 directives:

    module
    mod
    toxtree
    index



文档构建和项目集成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

一般会把编译生成文档，把文档挂到文档托管平台（比如对于开源项目可以使用 readthedocs 服务）的流程放进持续集成配置中。
这样做之后，文档每次更新都能及时反映给文档的读者。
开源项目可以免费使用 Travis 提供的持续集成服务。

参考文献
=========

- Sphinx: http://www.sphinx-doc.org/en/master/
- Sphinx 文档模板：http://graceful.readthedocs.io/en/latest/
- recipe 模板： http://code.activestate.com/recipes/langs/python/
- reStructuredText premier: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
- reStructuredText 幻灯片: http://docutils-zh-cn.readthedocs.io/zh_CN/latest/user/slide-shows.html#features-2-handouts
- readthedocs 文档托管平台： https://readthedocs.org/
- Travis: https://www.travis-ci.org/getting_started

.. _Sphinx: http://www.sphinx-doc.org/en/master/
.. _reStructuredText Premier: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html