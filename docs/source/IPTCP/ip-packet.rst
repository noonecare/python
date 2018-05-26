===========
IP packet
===========

:Author: 王蒙
:Tags: 网络协议，网络编程

:abstract:

    介绍 IP packet 中包含哪些字段，这些字段有什么用

.. contents::

Audience
========

运维，网络应用开发者

Prerequisites
=============


Problem
=======

IP packet 中有哪些字段，这些字段有什么用


Solution
========

IP packet 中包括 **IP 头** 和 **数据**。数据就是要传输的消息。

IP 头长为 20 字节，除非有选项字段。

IP 头中包含的字段有：

- 4 位版本: 表明是 IPv4 还是 IPv6。
- 4 位头长度: 表明 IP 头长度（32 bit 为单位），因为 IP 可能包含选项字段，所以是变长的。因为只有4位，所以TCP首部最长60字节。
- 16位总长度： 表明包含数据在内的总长度（字节数）。
- 16位标识：IP packet 的唯一标识，因为 IP packet 在传输过程中，可能会分片，可能需要重新组装。所以需要 IP packet 的唯一标识。
- 3 位标志：

    - 一个位表示是否还有 **更多片段**，如果还有就该该比特位设成 1， 否则设成 0 。
    - 不分片位，设为1时，强制不分片。如果必须分片，就丢弃该 IP packet, 并发送 ICMP 报文。


- 13 位片偏移：

    - 该 IP packet 片相对于原来 IP packet 的偏移量。

- 8 位生存时间（TTL）：IP packet 可以经过的最多路由器数目。TTL 的初始值由源主机设置，一旦经过一个处理它的路由器，它的值就减去1。当该字段的值为0时，IP packet 就会被丢弃。
- 8 位协议：传输采用的一些，比如 ICMP, IGMP, TCP, UDP 等等。
- 16 位头部校验和：校验IP packet 是否被篡改。如果发现被篡改了，那么 IP packet 会被丢弃，一般还会被重传。
- 32 位源IP地址。
- 32 位目的IP地址。
- 选项（可选）：略




Reference
=========

Put here references, and links to other documents.
