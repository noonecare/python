================
sphinx
================

:作者: 王蒙
:标签: docstring, api doc, search, sphinx

:简介:

    使用 sphinx 生成 Python 项目项目文档。

.. contents::

目标读者
==========

Python 开发

预备知识
=============

reStructured Text

问题
=======


解决办法
==========

sphinx 兼容了 reStructured Text 所有的标记语法。除此之外，sphinx 提供了新的 Markup/Directives, 而且可以配置不同的 extensions 以支持新的 Markup/Directives。

sphinx 命令
-------------------

参考 `初入 Sphinx` 学习使用 sphinx-quickstart, sphinx-build, sphinx-apidoc 。

sphinx-quickstart 用于快速生成 **conf.py**, **index.rst** 等配置文件。
sphinx-build 根据配置文件，生成 html，pdf 等等多种格式的文档。
sphinx-apidoc 根据源码，生成 rst 文件。该文件中包括 **automodule**, **autofunction** 标记（Markup）, 如果在配置文件中激活 **sphinx.ext.autodoc**, sphinx 就能提取源码的 docstring ，把源码中的 docstring 显示到生成的展示文件中。sphinx 提取源码中的 docstring 时, 可能需要修改 conf.py 文件中的 sys.path ，确保 sphinx 能够找到该模块（module）。



sphinx 配置文件
---------------------

sphinx-quickstart 和 sphinx-apidoc 是为了方便，不嫌麻烦完全可以自己写 **conf.py**, **index.rst** 文件。




sphinx 重要的标记（Markup）
-------------------------------


之前踩过的坑
-------------------------------

最佳实践
--------------------------------

参考文献
=========

- 初入 Sphinx: http://www.pythondoc.com/sphinx/tutorial.html