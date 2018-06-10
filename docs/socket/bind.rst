===========
bind
===========

:Author: 王蒙
:Tags: 网络编程

:abstract:

    socket 一定要绑定到网络接口上才能完成通信，绑定到哪个网络接口，绑定到哪个端口，有些坑需要注意。

.. contents::

Audience
========

网络编程

Prerequisites
=============

- 网络接口

Problem
=======

- 怎样绑定，使得 socket 只能和本地主机通信？
- 127.0.0.1， 0.0.0.0 和 localhost 的区别？
- 端口号使用有哪些惯例？



Solution
========

socket 的 `bind` 方法提供了绑定端口的功能。注意绑定的是网络接口，不是主机，一台主机通常有多个网络接口。

- 怎样绑定，使得 socket 只能和本地主机通信？

    主机都有lo网络接口，比如在 linux 上输入 `ifconfig` 就能找到该网络接口。

    .. code-block::

        $ ifconfig
        lo:    flags=73<UP,LOOPBACK,RUNNING> mtu 65535
                inet 127.0.0.1    netmask 255.0.0.0
                inet6 ::1  prefix 128  scopeid  0x10<host>
                loop txqueuelen 1 (Local Loopback)
                RX packets 3021 bytes 244698 (238.9KiB)
                RX errors 0 dropped 0 overruns 0 frame 0
                RX packets 3021 bytes 244698 (238.9KiB)
                RX errors 0 dropped 0 overruns 0 frame 0

    - 绑定到 **127.0.0.1** (lo 网络接口) 的 socket, 只能在本地进行通信。
    - 绑定到其他 ip 的 socket, 能在什么范围通信，需要看该 ip 对应网络接口的 scopeid。
    - 绑定到 **0.0.0.0** 的 socket, 能够通过所有该主机可用的网络接口进行通信。


- 127.0.0.1， 0.0.0.0 和 localhost 的区别？

    localhost 是 127.0.0.1 的域名。
    0.0.0.0 可以走任意网络接口。
    127.0.0.1 只能走 lo 网络接口，只能本地通信。


- 端口号使用有哪些惯例？

    端口号分三类：

        - Well Know Ports: 0-1023 端口，这些端口提供指定的服务。比如：
            - TELNET : 23
            - SMTP : 25
            - DNS : 53
            - HTTP : 80

        - Register Ports: 1023-49151 端口，自己写的服务器绑定这些端口，对外提供服务。

        - Ephemeral Ports: 49152–65535 端口。随意使用的 ports。比如客户端访问互联网，并不需要指定端口，操作系统会自动从 Ephemeral
          Ports 中随机取一个端口使用。

Reference
=========

- Foundations of Python Networks Programming
