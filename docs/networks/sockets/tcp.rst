===========
TCP
===========

:Author: 王蒙
:Tags: 网络编程

:abstract:

    介绍处理 tcp socket 时的注意事项。tcp 是可靠的，面向连接的通信协议。

.. contents::

Audience
========

网络编程

Prerequisites
=============

socket,udp

Problem
=======


- tcp 连接
- tcp 处理数据需要注意什么
- python tcp api


Solution
========

- tcp 连接

    tcp 通过有名的三次握手完成连接。调用 sock.connect 建立连接。
    tcp 通过有名的四次挥手关闭连接。在关闭连接时，有 HALF-CLOSE 状态。socket 可以配置处理 HALF-CLOSE 状态的行为。


- tcp 处理数据需要注意什么

    tcp socket 保证了消息可靠的传输到对面 socket（操作系统给完成的，不需要编程的人自己操心）。

    但是 tcp socket 不保证每次收发完整的一条消息。tcp 每次收发都从 incoming buffer/outgoing buffer 中读取/写入一段字节的数据。是否是完整的一条消息，需要编程的人自己定义。

    实际上 tcp socket 编程中最大部分的逻辑就是定义如何确定收到了/发送了完整的一条的消息（这部分逻辑称为 Framing）。


    http 协议的 Framing 逻辑，可以为我们自定义 Framing 逻辑提供借鉴。比如

    - 长度为固定长（比如 16byte） 的消息是一条完整的消息。
    - 使用特定的 delimiter (比如 \r\n) 分割不同的消息。
    - 使用自带



    如果 socket A 不断向 socket B 发送数据，但是 socket B 从不执行 recv()，socket B 只是不断地向 socket A 发送数据。那么就会导致 socket A 的 outgoing buffer 和 socket B 的 incoming buffer 被填满。填满之后，就不能再收发数据，导致了死锁。

    tcp socket 可以关闭单个方向的数据传输。

- python tcp api

    .. code-block::

        # 侦听连接请求，sock 一旦执行了下面的方法，就决定了这是 passive socket。
        # listen(backlog)  中的 backlog 参数，表示能接受的最大等待处理（等待执行 accept 方法）连接数。如果等待处理的连接数超过了backlog 就会报 Connection Refused 异常。
        # 可以写代码测试下，一个 passive socket 最多能 accept 多少个 connection？linux 貌似有配置文件，写明了最多建立多少个 connections。
        sock.listen(1)

        # passive socket 执行 accept 方法，返回负责处理和 client 的 conversation 的 conversation_sock 以及 client 的 address
        # 特别插一句，conversation_sock 和 passive socket 的 (ip, port) 是一样的。
        conversation_sock, address = sock.accept()

        # send() 返回实际传输的二进制串的长度，一定注意 send(msg) 不一定就能完整地把 msg 传输走。
        # 一般 send(msg) 能够很快返回，但是如果 outgoing buffer 是满的，那么 send() 就会卡住。
        sock.send(msg)

        # socket 提供了 sendall 方法，使得我们不用为了完整地把数据 send 出去，而写循环。
        sock.sendall(msg)

        # recv(MAX_BYTES) 返回实际接收到的 bytes。因为一般不能完整的读取一条消息，所以， recv 一般都会用到 while 循环。没有 recvall 方法，因为没法提前预判自己要接收多少字节的数据。
        sock.recv(MAX_BYTES)

        # 可以像读文件一样，读 tcp socket。
        f = sock.makefile()
        f.write(b'blablabla')
        f.read()

        # shutdown 用来关闭 socket 某个方向的数据传输
        sock.shutdown(SHUT_WR)  # sock 不会再发送数据了
        sock.shutdown(SHUT_RD)  # sock 不会再收数据了
        sock.shutdown(SHUT_RDWR)  # sock 不再发数据，也不再收数据了

        # 在建立 socket 时，常常进行如下的设置。
        # 当这样设置的 sock 建立至少一个连接之后，CTRL+C 关闭 sock 之后，sock 使用的端口号能够立即被使用。
        # 如果不这样设置，sock 建立至少一个连接之后，CTRL+C 关闭 sock 之后，sock 使用的端口不能立即被使用。
        # 我猜测这跟四次挥手有关。
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 连接到 tcp 服务器
        sc.connect((host, port))

        # 关闭 socket
        sc.close()





Reference
=========

- Foundations of Python Network Programming
