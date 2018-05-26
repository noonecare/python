===========
Route
===========

:Author: 王蒙
:Tags: 网络协议

:abstract:

    IP 路由

.. contents::

Audience
========

运维，网络应用开发

Prerequisites
=============

IP,子网等。


Problem
=======

IP 如何根据路由表路由？
如何修改 IP 路由表？


Solution
========

.. code-block::

    vagrant@precise64:~$ route
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    default         localhost       0.0.0.0         UG    0      0        0 eth0
    default         localhost       0.0.0.0         UG    100    0        0 eth0
    10.0.2.0        *               255.255.255.0   U     0      0        0 eth0



#. frame 中目的IP 地址始终不变，整


Reference
=========

Put here references, and links to other documents.
