===========
UDP
===========

:Author: 王蒙
:Tags: 网络编程

:abstract:

           udp 只剩下广播功能比较有用，其他的都被 tcp 替代了。简要了解下 udp 即可。

.. contents::

Audience
========

网络编程

Prerequisites
=============

socket,子网

Problem
=======

- udp 有哪些特点
- python udp api


Solution
========

- udp 有哪些特点？

    udp (user datagram protocol) 能够保证数据的完整性（每次传递一个 datagram），但是不保证消息一定可靠地传输到对面 socket，需要用户自己写代码保证数据可靠地传输到了对面的socket。

    不可靠意味着：

        - datagram 可能会丢失
        - datagram 可能会重复
        - datagram 可能失序


    udp 可以广播（发送一条消息，子网中的所有主机都能收到该消息），tcp 不能，要发送广播需要把消息发给广播地址。

    广播地址是子网中的最大地址（网关地址是子网中的最小地址），比如说在 192.168.122.1/24 网络中，广播地址是 192.168.122.255（网关地址是 192.168.122.1）。在 linux 中，输入 `ifconfig` 命令，返回的结果中的 broadcast 后面的 ip 就是该网卡所在子网的广播地址。

- python udp api

    在使用 python udp api 上，要注意：

        - udp 不是面向连接的，所以不用建立连接就可以通信。
        - udp 需要编程的人自己去保证数据没有丢失，没有重复，没有失序。

    .. code-block::

        # 创建 udp socket.
        sock = socket(socket.AF_INET, socket.SOCK_DGRAM)
        # recvfrom 每次接收一个完整的 datagram（和 tcp 接收不定长的 stream 不同）
        data, address = sock.recvfrom(MAX_BYTES)
        # sendto 每次发送一个完整的 datagram(和 tcp 发送不定长的 stream 不同)
        sock.sendto(message, address)
        # connect 在 tcp 中的含义是通过三次握手建立连接，在 udp 中，只是一个语法糖。
        # 该语法糖使我们可以使用 recv, send 收发消息，且在收发数据时，只能和 connect 的主机收发消息（比如说如果有其他的主机向 udp
        # 服务器发送消息，那么 udp 服务器不接收该消息）。
        sock.connect(address); sock.send(message); sock.recv(MAX_BYTES)
        # 因为 udp 可能丢包，所以要设置 timeout, 不然，一个包丢了可能让程序卡死。
        sock.settimeout(delay)
        # 可以效仿 tcp 使用 exponential backoff 的方式，不断重发 datagram 确保 datagram 能够传输到对面。
        # 对于 exponential backoff 的方式，我举个例子。第一次发送数据之后，设置 timeout 为 0.2 秒，如果 0.2 秒还没有收到回复。
        # 那么重发，并设置 timeout 为 0.4 秒，如果0.4 秒还没有收到回复，那么设置 timeout 为 0.8 秒，重发， 依次类推，每次 timeout
        # 是上一次的 2 倍。如果成功接收到回复，停止重发；如果timeout 超过某个阈值（比如 10 秒）还是收不到回复，报错退出。
        # 参照 `实现了 exponential backoof 的代码`_ 学习 exponential backoff 。

        # 可以在 datagram 中添加 request_id 来解决失序和重复的问题。有了 request_id ，对接收到的 datagram 按照 request_id 排序，
        # 就解决了失序和重复的问题。这其实也是仿照 tcp 的实现，tcp packet 中有 sequence_id 字段，和这里的 request_id 基本上一样。
        # 真是应了那句话： 每次写 udp 程序，总感觉自己在自定义 tcp。

        # 上面的 exponential backoff, request_id 在实践中几乎用不到，因为明显直接用 tcp 会更好。
        # 但是 udp 可以广播，这是 tcp 做不到的。
        # udp 要做广播，需要配置下 socket（让socket 支持广播），然后 socket 应该向 broadcast 地址发消息。
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(192.168.122.255)  # broadcast 是子网中的最大地址。
        # 阅读 `udp_broadcast.py`_ 学习 broadcast。





Reference
=========



.. _实现了 exponential backoof 的代码: https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter02/udp_remote.py
.. _udp_broadcast.py: https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter02/udp_broadcast.py