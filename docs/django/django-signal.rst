================
Django Signal
================

:作者: 王蒙
:标签: django, signal

:简介:

    Django 中的 signal 类似于 hook。signal 能够让一个事件，触发多个操作。

.. contents::

目标读者
==========

Django 网站开发

预备知识
=============


问题
=======

Django signal

signal handlers


解决办法
==========

Django signal
~~~~~~~~~~~~~~~~~~~~

Django 自带的 signal:

    Model： pre_save, post_save, pre_delete, post_delete, m2m_changed

    requests: request_started, request_finished

    可以自定义 signal, 触发信号，使用如下代码：


        .. code-block:: python

            from .signals.signals import my_signal

            my_signal.send(sender="some function or class",
                           my_signal_arg1="something", my_signal_arg_2="something else"])

signal handlers
~~~~~~~~~~~~~~~~~~~~~~~~~

django.dispatch.receiver 绑定 singal handler 函数。



参考文献
=========

- How to use signal in Django: http://sabinemaennel.ch/django/signals-in-django/