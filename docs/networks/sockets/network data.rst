============
network data
============

:Author: 王蒙
:Tags: 网络编程

:abstract:

    网络上常见的数据格式。处理这些数据涉及到统一格式的问题。

.. contents::

Audience
========

网络编程

Prerequisites
=============




Problem
=======

网络上传输数据的常见格式有哪些？

Solution
========

网络上传输的都是 **bytes**, 不是字符串。

接收到 bytes 之后，一般需要反序列化为 python 对象来处理。

在处理的过程中涉及到统一数据格式的问题。

网络传输字符串时，可能会采用 **特定的编码** （比如 ascii 和 utf-8）， 处理时，需要使用正确的编码解码。

网络传输数字时，可能采用 **大端机** 的顺序，也可能采用 **小端机** 的顺序，需要根据具体情况解码出数字。 python `struct` 包能完成数字转成大端机编码和小端机编码的任务。

网络传输的数据时，也可能传输的是用 pickle 序列化的数据。pickle 是 **self-delimiting** 的格式，方便 tcp 读写时，识别完整的一条消息。

网络传输数据时，也常常采用 XMl 和 JSON 格式，注意采用合适的包反序列化。

网络传输数据，可能会选择压缩数据。压缩格式一般是 **self-delimiting** 的，这方便了 tcp 读写时，识别完整的一条消息。




Reference
=========

- Foundations of Python Networks Programming
