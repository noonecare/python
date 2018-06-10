============
ARP protocol
============

:Author: 王蒙
:Tags: 网络协议，网络编程

:abstract:

    ARP 是什么？
    为什么需要 ARP?

.. contents::

Audience
========

运维，网络应用开发者

Prerequisites
=============

Write the list of prerequisites for implementing this recipe.  This
can be additional documents, software, specific libraries, environment
settings or just anything that is required beyond the obvious language
interpreter.


Problem
=======

    - ARP 是什么？
    - 为什么需要 ARP?


Solution
========

ARP 是什么？

    ARP 把 32 位 IP 地址转成 48 位以太网地址；
    RARP 把 48 位以太网地址转成 32 位 IP 地址。


为什么需要 ARP?

    当一台主机把以太网数据帧发送到同一局域网上的另一台主机时，是根据 48 bit 的以太网地址来确定目的接口的。设备驱动程序从不检查 IP 数据报中的目的IP地址。
    就是说目的 IP 负责选择 route 路径，以太网地址负责送以太网数据帧到指定的主机。

ARP 怎么做？

步骤：

    #. 在局域网广播 ARP请求， ARP 请求帧中包含目的主机的 IP 地址，其意思是 “如果你是这个 IP 地址的拥有者，请回答你的硬件地址”。

    #. 匹配 ARP 请求中的 IP 地址的目的主机，发送一个 ARP 应答。这个应答中包含 IP 地址及对应的硬件地址。

ARP 请求和应答：

    .. image:: ARP.png






ARP 告诉缓存？

    ARP IP 地址和硬件地址的对应表会被缓存一段时间，以提高效率。 arp -a 显示缓存的对应表。

    .. code-block:: shell

        % arp -a
        sun (140.252.13.33) at 8:0:20:3:f6:42
        svr4 (140.252.13.34) at 0:0:c0:c2:9b:26



Reference
=========

Put here references, and links to other documents.


.. _ARP 请求和应答字段: ./ARP.png