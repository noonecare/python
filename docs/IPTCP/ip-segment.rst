=============
IP 分片和重组
=============

:Author: 王蒙
:Tags: 网络协议，网络编程

:abstract:

    介绍 IP packet 的分片和重装。

.. contents::

Audience
========

运维，网络开发者

Prerequisites
=============

了解 IP packet。


Problem
=======

为什么要分片，如何实现分片？


Solution
========

网络接口对于传输包有大小限制（MTU），如果 IP packet 太大就要进行分片处理，每个pain独立地传送到目的地。到了目的地再重装成原来的
IP packet。

IP packet 中有：

    - 16 位标识位： 分片所属 IP packet 的标识符。
    - 3 位标志位: 是否有更多片段。
    - 13位片偏移量： 分片相对于原始 IP packet 的偏移量。

明显有了这三个量，就能把分段重装成原来的 IP packet。


Reference
=========

Put here references, and links to other documents.
