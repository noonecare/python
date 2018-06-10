===========
Django
===========

:Author: 王蒙
:Tags: 网络编程

:abstract:

    django 是 python 中最火的插件。

.. contents::

Audience
========

网络编程，python 编程

Prerequisites
=============

Python 语法，SQLAlchemy, 简单的JavaScript


Problem
=======

- django 中重要的组件
- django 的优势
- django 中常用的插件


Solution
========

django 的优势

django 的优势在于丰富的插件。开发一个小网站，也需要完成很多的功能（比如登录，认证，权限，处理数据库等等）。对于常见功能 django 中有现成的插件可用。我认为丰富的插件，是 django 好使的原因。


django 中重要的组件

MVT(Model, View, Template) 是django 中最重要的组成部分， M 表示后台数据， View 表示逻辑控制单元，Template 负责前端呈现。有这三个组件使的 django 能够完成网站开发的整个过程（本来需要分成前端和后端的）。


- view

    和 flask, tornado 一样，负责解析 request 构造 response。

- urls

    根据 url 中的 path， route 请求到各自的 view 处理。

- settings

    配置（下面使用插件会详细说明）。

- template

    template 通过 render 函数，把后台程序的变量传递给前端页面，实现些逻辑功能等。

- models

使用插件

Reference
=========

- Django模板中常用的标签(tag): https://blog.csdn.net/you_are_my_dream/article/details/53056141
- Django模板中常用过滤器(filter): https://blog.csdn.net/you_are_my_dream/article/details/53066654
