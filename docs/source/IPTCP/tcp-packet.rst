===========
TCP packet
===========

:Author: 王蒙
:Tags: 网络协议，网络编程

:abstract:

    介绍 TCP packet 中重要的字段。

.. contents::

Audience
========

网络应用开发者

Prerequisites
=============

Write the list of prerequisites for implementing this recipe.  This
can be additional documents, software, specific libraries, environment
settings or just anything that is required beyond the obvious language
interpreter.


Problem
=======

TCP packet 包括 **TCP 头** 和 **TCP 数据**。如果不含任选字段，TCP 头是 20 字节。

TCP 头包括：

    - 16 位源端口号。
    - 16 位目的端口号。
    - 32 位序号。
    - 32 位确认序号。
    - 4 位头长度， 以 32 bit 位单位。
    - 6 位保留字段。

        - URG: 紧急指针有效。
        - ACK: 确认序号有效。
        - PSH: 接受方应该尽快将这个报文段交给应用层。
        - RST: 重建连接。
        - SYN:
        - FIN: 完成。
    - 16 位窗口大小。
    - 16 位校验和。
    - 16 位紧急指针。
    - 选项。




Solution
========

Give solution to problem explained earlier.  This is the core of a
recipe.


Reference
=========

Put here references, and links to other documents.
