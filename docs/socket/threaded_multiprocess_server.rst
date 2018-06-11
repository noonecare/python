=============
多线程服务器
=============

:作者: 王蒙
:标签: 多线程，服务器，WSGI

:abstract:

    Python 多线程（进程）服务器。

.. contents::

目标读者
========

Python 网站开发

预备知识
=============

wsgi, socket, 多线程


问题
=======

- 多线程服务器的优势和劣势？

- WSGI 相关的服务器和框架等？



解决办法
========

多线程服务器的优势和劣势？

    和 async 服务器相反，多线程服务器性能上略有不足。但是多线程服务器一般支持 WSGI 接口协议，所以可以和支持 WSGI 接口协议的 Web Application 兼容。简单点说，就是支持 WSGI 协议的 Web Application 可以在所有的支持 WSGI 接口协议的服务器上跑。

    支持 WSGI 接口协议的 Web Application 非常丰富，很多功能有现成的实现，所以使用多线程服务器，易于扩展功能。

WSGI 相关的服务器和框架？

    实际开发过程中，几乎不用写服务器，基本上都是使用现成的服务器。Python 中有名的支持 WSGI 的服务器有：

        - `gunicorn`_

        - `uWSGI`_

    实际开发中，主要写的是 Application。写 WSGI Application 的框架包有很多。比如：

        - Django
        - werkzueg
        - webob

    写 WSGI Application 的内容，查看 `wsgi`_ 。

Reference
=========

.. _gunicorn: http://gunicorn.org/
.. _uWSGI: http://uwsgi-docs.readthedocs.io/en/latest/
.. _wsgi: ../web_app/wsgi.rst