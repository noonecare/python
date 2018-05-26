===========
frame
===========

:Author: 王蒙
:Tags: 网络协议，网络编程

:abstract:

    网络是一帧一帧数据传输的。常见的抓包工具，抓到的一个包，其实就是一帧数据。这个小节，介绍下帧的组成。

.. contents::

Audience
========

运维，网络开发者等。

Prerequisites
=============



Problem
=======

帧（Frame）有哪些部件组成。

Solution
========

帧（Frame）包含：

    - 以太网头部

        -

    - IP 头
    - TCP 头或者 UDP 头
    - 应用数据
    - 以太网尾部

帧的组成，刚好对应四层网络结构。

Reference
=========

Put here references, and links to other documents.
