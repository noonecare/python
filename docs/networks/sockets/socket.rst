===========
socket
===========

:Author: 王蒙
:Tags: 网络编程

:abstract:

    socket 是对于网络传输层的抽象，可以用来实现网络传输层及其之上的网络协议。

.. contents::

Audience
========

网络开发

Prerequisites
=============

IP, port, 网络四层结构


Problem
=======

- socket 是什么
- socket 有哪几种
- socket 编程有什么用
- socket python API

Solution
========

- socket 是什么？

    通常说网络有四层抽象（链路层，网络层，传输层和应用层）。

    网络层实现了点到点（主机到主机）的通信，网络层中主要的协议是 IP 路由协议。传输层，实现了端到端的通信。

    socket 是对于传输层的抽象，socket 代表了网络中的端。

    socket 一定有 IP（IP 地址） 和 port（端口号）。不过需要注意，多个 socket 可能对应同一个 (IP, port)，可以认为 socket 由 (source_ip, source_port, des_ip, dest_port) 唯一确定。

    socket 支持读(recv)写(send, sendall)， 是大小可变长的文件描述符。

- socket 有哪几种？

    active socket: 主动发起通信的 socket。
    passive socket: 侦听 active socket 连接请求的连接，从代码中看，就是执行 `listen` 方法的 socket。passive socket 只负责侦听，不会实际负责具体的会话（conversation）。
    connected socket: passive socket 侦听到客户端的连接，调用 `accept` 方法返回 connected socket（会和 passive socket 具有相同的 (ip, port)），connected socket 负责和客户端会话(conversation)。

- socket 编程有什么用？

    理论上，socket 编程可以实现网络传输层及其之上的所有协议。但是因为 socket 是对于网络过于底层的抽象导致直接用 socket 实现应用需要过多的劳动。所以 socket 编程主要用于自定义网络协议。

    针对特定的任务，有时候需要自定义网络协议。比如 Message Queue，RPC 等协议都可以用 socket 编程实现。

- socket python api?

    python socket api 和操作系统提供的 socket api 几乎一样。比较明显的区别是， python socket api 中定义了 socket 类型，但是操作系统 socket api 中的 socket 就是一个 fileno。

    socket python api 中重要的 api 有：

        - bind
        - connect
        - accept
        - listen
        - setopts
        - recv
        - send
        - sendall


Reference
=========

- Foundations of Python Networks Programming
- TCP/IP 协议详解 卷1
