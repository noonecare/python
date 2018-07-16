================
Deploy Django
================

:作者: 王蒙
:标签: Django, WSGI, Deploy

:简介:

    怎样部署 Django, 更准确地说怎样部署 WSGI Application.

.. contents::

目标读者
==========

后端开发

预备知识
=============

WSGI

问题
=======

- Apache wsgi_mod
- gunicorn
- uWSGI

解决办法
==========

Django 是 WSGI Application。可以采用部署 WSGI Application 的方法来部署 Django 应用。

Django 本身提供的 Server 用于开发（测试和调试）。Django 本身提供的 Server 不能用于部署，因为该 Server 性能不行。应该使用部署 WSGI 应用的方法，部署 Django 应用。

常见部署 WSGI 应用的方法有：

- Apache wsgi_mod

- Python WSGI Server:

    - gunicorn
    - uWSGI



参考文献
=========

