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

sphinx-apidoc 根据源码，生成 rst 文件。该文件中包括 **automodule**, **autofunction** 标记（Markup）, 如果在配置文件中激活 **sphinx.ext.autodoc**, sphinx 就能提取源码的 docstring ，把源码中的 docstring 显示到生成的文档中。sphinx 提取源码中的 docstring 时, 可能需要修改 conf.py 文件中的 sys.path ，确保 sphinx 能够找到该模块（module）。

sphinx 配置文件
---------------------

sphinx-quickstart 和 sphinx-apidoc 是为了方便，不嫌麻烦完全可以自己写 **conf.py**, **index.rst** 文件。




sphinx 重要的标记（Markup）
-------------------------------

mod
module
function
index
include

todo: 看 flask 的文档，看 flask 文档 source code, 比对出常用标记的含义。


之前踩过的坑
-------------------------------

使用 sphinx-apidoc 生成 python 模块的文档，使用 sphinx-build 编译出的 html 文档中，看不到 python 模块中的 docstring 。

    sphinx-apidoc 是根据 python 模块生成使用了 `automodule`, `autofunction` 等等标记（autodoc 模块支持的标记）的 rst 文档。要让这些标记生效有两点要求：

    - conf.py 中激活 autodoc 模块
    - sphinx 能够找到（引用）该 module（才能从该 module 中抽取 docstring）


使用中文？

    写中文文档，把 language 设成 zh（之间我一直language=chinese ，chinese sphinx 不认的，sphinx 认为 zh 是中文） ，生成的 sphinx 文档会比较好看（使用英文的话，中英文间杂着不好看）。

怎样 viewcode?

    如果只是 API 文档要添加 view code 的功能，非常简单，就是在 conf.py 中激活 sphinx.ext.viewcode 模块即可。



最佳实践
--------------------------------

从 rst 编译 html（以及其他格式的文档）时，使用 -W 参数

    -W 使得编译会把 warning 当成 error 处理。这样，能很容易找到所有 warning 和 error。否则，有些warning 导致的细节一直不出效果，不太容易找这些 warnings。

自动化生成文档的步骤，把生成文档的脚本写到 tox.ini 中



参考文献
=========

- 初入 Sphinx: http://www.pythondoc.com/sphinx/tutorial.html