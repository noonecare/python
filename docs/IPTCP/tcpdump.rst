===========
tcpdump
===========

:Author: 王蒙
:Tags: Linux, 网络协议，网络编程

:abstract:

    tcpdump 是 linux 中的抓包工具。使用这个工具，能直观地理解 TCP/IP 中的很多概念。

.. contents::

Audience
========

Linux 运维，网络应用开发者

Prerequisites
=============

简单的 linux 操作。

Problem
=======

如何使用 tcpdump 抓包？

- 抓取
- 过滤
- 保存和分析


Solution
========

.. code-block:: shell

    # tcpdump 需要 sudo 权限，所有之后的脚本都会带上 sudo
    # 查看所有网络接口, any 接口表示所有接口
    $ sudo tcpdump -D
    1.eth0
    2.any (Pseudo-device that captures on all interfaces)
    3.lo
    # 抓取通过指定网络接口(比如 eth0 网络接口)的包
    # -c 5 表示抓到 5 个包，就停止抓取
    $ sudo tcpdump -i eth0 -c 5
    ...
    # 抓取通过任意网络接口的包
    $ sudo tcpdump -i any -c 5
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    13:31:13.146724 IP 10.0.2.15.ssh > 10.0.2.2.64407: Flags [P.], seq 2565789445:2565789613, ack 21252087, win 22032, length 168
    13:31:13.146919 IP 10.0.2.2.64407 > 10.0.2.15.ssh: Flags [.], ack 168, win 65535, length 0
    13:31:13.147110 ARP, Request who-has 10.0.2.3 tell 10.0.2.15, length 28
    13:31:13.147189 ARP, Reply 10.0.2.3 is-at 52:54:00:12:35:03 (oui Unknown), length 46
    13:31:13.147197 IP 10.0.2.15.51011 > 10.0.2.3.domain: 58957+ PTR? 2.2.0.10.in-addr.arpa. (39)
    5 packets captured
    12 packets received by filter
    0 packets dropped by kernel

    # capture size 65535 bytes, 表示每个包最多抓取 65536 byte。IP 包最大 65536 bytes 所以这意味着全抓。可以使用 -s 指定抓取大小。
    # 每个包抓取头 96 bytes。
    $ sudo tcpdump -i any -c 5 -s 96
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on any, link-type LINUX_SLL (Linux cooked), capture size 96 bytes
    13:35:40.944878 IP 10.0.2.15.ssh > 10.0.2.2.64407: Flags [P.], seq 2565790245:2565790285, ack 21252295, win 22032, length 40
    13:35:40.945084 IP 10.0.2.2.64407 > 10.0.2.15.ssh: Flags [.], ack 40, win 65535, length 0
    13:35:40.945482 IP 10.0.2.15.52160 > 10.0.2.3.domain: 36116+ PTR? 2.2.0.10.in-addr.arpa. (39)
    13:35:40.985494 IP 10.0.2.3.domain > 10.0.2.15.52160: 36116 NXDomain 0/1/0 (89)
    13:35:40.985671 IP 10.0.2.15.49613 > 10.0.2.3.domain: 47324+ PTR? 15.2.0.10.in-addr.arpa. (40)
    5 packets captured
    19 packets received by filter
    0 packets dropped by kernel
    # 抓取结果中，第一列是抓取时间，第二列是该包采取的协议，第三列是源 socket(主机地址和端口号)，第四列是目标socket(地址和端口号)。
    # 上面结果中主机地址是域名，端口号是应用名。如果想使用IP 地址和数字形式的端口号，需使用 -n 选项。
    $ sudo tcpdump -i any -c 5 -n
    listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    13:39:14.240890 IP 10.0.2.15.22 > 10.0.2.2.64407: Flags [P.], seq 2565791277:2565791301, ack 21252919, win 22032, length 24
    13:39:14.241081 IP 10.0.2.2.64407 > 10.0.2.15.22: Flags [.], ack 24, win 65535, length 0
    13:39:14.241202 IP 10.0.2.15.22 > 10.0.2.2.64407: Flags [P.], seq 24:112, ack 1, win 22032, length 88
    13:39:14.241337 IP 10.0.2.2.64407 > 10.0.2.15.22: Flags [.], ack 112, win 65535, length 0
    13:39:14.241470 IP 10.0.2.15.22 > 10.0.2.2.64407: Flags [P.], seq 112:168, ack 1, win 22032, length 56
    5 packets captured
    6 packets received by filter
    0 packets dropped by kernel
    # 第五列表示消息的Flag 信息，具体来说 P 表示 PSH, . 表示 ACK, S 表示 SYN, F 表示 FIN, R 表示 RST， U 表示 URG（刚好是 IP 头中的 6 个保留位）。
    # 第六列表示 sequence number: acknowledge number, 除了第一列完整显示之外，下面的列都是用相对值。第七列表示 window size。第八列表示包的大小，
    # 刚好等于 acknowledge number - sequence number。
    # todo: window size 我不理解，需要我再研究下。


    # 使用过滤，可以使我们专注观察我们感兴趣的包。不然那么多包，把关注点给隐藏了。
    # host, 选通过某个 host 的包
    # src host, 选从某个 host 发出的包
    # des host, 选被某个 host 接受的包
    $ sudo tcpdump -i any -c 5
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    14:00:58.192522 IP 10.0.2.15.ssh > 10.0.2.2.64407: Flags [P.], seq 2565794341:2565794365, ack 21254391, win 22032, length 24
    14:00:58.192638 IP 10.0.2.15.ssh > 10.0.2.2.64407: Flags [P.], seq 24:48, ack 1, win 22032, length 24
    14:00:58.192693 IP 10.0.2.2.64407 > 10.0.2.15.ssh: Flags [.], ack 24, win 65535, length 0
    14:00:58.192702 IP 10.0.2.2.64407 > 10.0.2.15.ssh: Flags [.], ack 48, win 65535, length 0
    14:00:58.192774 IP 10.0.2.15.ssh > 10.0.2.2.64407: Flags [P.], seq 48:72, ack 1, win 22032, length 24
    5 packets captured
    31 packets received by filter
    0 packets dropped by kernel
    $ sudo tcpdump -i any -c 5 host 119.75.213.61
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    14:01:08.443447 IP 10.0.2.15 > 127.0.0.1: ICMP echo request, id 1338, seq 58, length 64
    14:01:08.453229 IP 127.0.0.1 > 10.0.2.15: ICMP echo reply, id 1338, seq 58, length 64
    14:01:09.444495 IP 10.0.2.15 > 127.0.0.1: ICMP echo request, id 1338, seq 59, length 64
    14:01:09.452179 IP 127.0.0.1 > 10.0.2.15: ICMP echo reply, id 1338, seq 59, length 64
    14:01:10.445870 IP 10.0.2.15 > 127.0.0.1: ICMP echo request, id 1338, seq 60, length 64
    5 packets captured
    5 packets received by filter
    0 packets dropped by kernel

    # 使用 port 选项，捕获通过指定端口的包
    $ sudo tcpdump -i any -c 5 -n port 80
    $ sudo tcpdump -i any -c 5 port 80 -n
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    14:05:28.479440 IP 10.0.2.15.39821 > 119.75.213.61.80: Flags [S], seq 2125492756, win 14600, options [mss 1460,sackOK,TS val 1012393 ecr 0,nop
    ,wscale 3], length 0
    14:05:28.489360 IP 119.75.213.61.80 > 10.0.2.15.39821: Flags [S.], seq 538112001, ack 2125492757, win 65535, options [mss 1460], length 0
    14:05:28.489387 IP 10.0.2.15.39821 > 119.75.213.61.80: Flags [.], ack 1, win 14600, length 0
    14:05:28.489624 IP 10.0.2.15.39821 > 119.75.213.61.80: Flags [P.], seq 1:114, ack 1, win 14600, length 113
    14:05:28.489805 IP 119.75.213.61.80 > 10.0.2.15.39821: Flags [.], ack 114, win 65535, length 0
    5 packets captured
    5 packets received by filter
    0 packets dropped by kernel

    # 选择 Flag
    $ sudo tcpdump -i any -c 10 "tcp[tcpflags] & tcp-syn != 0"
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    15:04:47.472034 IP 10.0.2.15.51509 > 10.136.7.81.ssh: Flags [S], seq 4251015673, win 14600, options [mss 1460,sackOK,TS val 1902142 ecr 0,nop,
    wscale 3], length 0
    15:04:48.471786 IP 10.0.2.15.51509 > 10.136.7.81.ssh: Flags [S], seq 4251015673, win 14600, options [mss 1460,sackOK,TS val 1902392 ecr 0,nop,
    wscale 3], length 0
    15:04:50.476360 IP 10.0.2.15.51509 > 10.136.7.81.ssh: Flags [S], seq 4251015673, win 14600, options [mss 1460,sackOK,TS val 1902893 ecr 0,nop,
    wscale 3], length 0
    15:04:54.488758 IP 10.0.2.15.51509 > 10.136.7.81.ssh: Flags [S], seq 4251015673, win 14600, options [mss 1460,sackOK,TS val 1903896 ecr 0,nop,
    wscale 3], length 0
    15:05:02.504585 IP 10.0.2.15.51509 > 10.136.7.81.ssh: Flags [S], seq 4251015673, win 14600, options [mss 1460,sackOK,TS val 1905900 ecr 0,nop,
    wscale 3], length 0


    # 使用 ascii 码显示包中的内容
    $ sudo tcpdump -i any -c 5 -A
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    15:07:05.941319 IP 10.0.2.15.ssh > 10.0.2.2.64407: Flags [P.], seq 2565812773:2565812797, ack 21263031, win 24624, length 24
    E..@..@.@.d.
    ...
    .........2%.Dr.P.`0.C..S,......O&{...c.%....S..
    15:07:05.941525 IP 10.0.2.2.64407 > 10.0.2.15.ssh: Flags [.], ack 24, win 65535, length 0
    E..(.5..@.O.
    ...
    ........Dr...2=P...\.........
    15:07:05.941674 IP 10.0.2.15.41571 > 10.0.2.3.domain: 40153+ PTR? 2.2.0.10.in-addr.arpa. (39)
    E..C.w@.@..!
    ...
    ....c.5./.R.............2.2.0.10.in-addr.arpa.....
    15:07:05.947887 IP 10.0.2.3.domain > 10.0.2.15.41571: 40153 NXDomain 0/1/0 (89)
    E..u.6..@.O1
    ...
    ....5.c.a...............2.2.0.10.in-addr.arpa......10.IN-ADDR.ARPA............'.......p.... .   :...Q.
    15:07:05.948125 IP 10.0.2.15.55537 > 10.0.2.3.domain: 11910+ PTR? 15.2.0.10.in-addr.arpa. (40)
    E..D.y@.@...
    ...
    ......5.0.S.............15.2.0.10.in-addr.arpa.....
    5 packets captured
    10 packets received by filter
    0 packets dropped by kernel

    # 使用 ascii + hex 的方式展示内容
    $ sudo tcpdump -i any -c 5 -XX
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    15:08:02.905565 IP 10.0.2.15.ssh > 10.0.2.2.64407: Flags [P.], seq 2565813213:2565813237, ack 21263151, win 24624, length 24
            0x0000:  0004 0001 0006 0800 2788 0ca6 0000 0800  ........'.......
            0x0010:  4500 0040 bdbb 4000 4006 64ec 0a00 020f  E..@..@.@.d.....
            0x0020:  0a00 0202 0016 fb97 98ef 33dd 0144 732f  ..........3..Ds/
            0x0030:  5018 6030 1843 0000 ddaa 9999 0604 c552  P.`0.C.........R
            0x0040:  3f2f 0b49 ce07 bab8 4b9a 0f9f 72ac adbc  ?/.I....K...r...
    15:08:02.905785 IP 10.0.2.2.64407 > 10.0.2.15.ssh: Flags [.], ack 24, win 65535, length 0
            0x0000:  0000 0001 0006 5254 0012 3502 0000 0800  ......RT..5.....
            0x0010:  4500 0028 1346 0000 4006 4f7a 0a00 0202  E..(.F..@.Oz....
            0x0020:  0a00 020f fb97 0016 0144 732f 98ef 33f5  .........Ds/..3.
            0x0030:  5010 ffff 5abe 0000 0000 0000 0000       P...Z.........
    15:08:02.905945 IP 10.0.2.15.33627 > 10.0.2.3.domain: 37078+ PTR? 2.2.0.10.in-addr.arpa. (39)
            0x0000:  0004 0001 0006 0800 2788 0ca6 0000 0800  ........'.......
            0x0010:  4500 0043 c518 4000 4011 5d80 0a00 020f  E..C..@.@.].....
            0x0020:  0a00 0203 835b 0035 002f 1852 90d6 0100  .....[.5./.R....
            0x0030:  0001 0000 0000 0000 0132 0132 0130 0231  .........2.2.0.1
            0x0040:  3007 696e 2d61 6464 7204 6172 7061 0000  0.in-addr.arpa..
            0x0050:  0c00 01                                  ...
    15:08:02.914533 IP 10.0.2.3.domain > 10.0.2.15.33627: 37078 NXDomain 0/1/0 (89)
            0x0000:  0000 0001 0006 5254 0012 3502 0000 0800  ......RT..5.....
            0x0010:  4500 0075 1347 0000 4011 4f20 0a00 0203  E..u.G..@.O.....
            0x0020:  0a00 020f 0035 835b 0061 9def 90d6 8183  .....5.[.a......
            0x0030:  0001 0000 0001 0000 0132 0132 0130 0231  .........2.2.0.1
            0x0040:  3007 696e 2d61 6464 7204 6172 7061 0000  0.in-addr.arpa..
            0x0050:  0c00 0102 3130 0749 4e2d 4144 4452 0441  ....10.IN-ADDR.A
            0x0060:  5250 4100 0006 0001 0000 2237 0017 c027  RPA......."7...'
            0x0070:  0000 0000 0000 0070 8000 001c 2000 093a  .......p.......:
            0x0080:  8000 0151 80                             ...Q.
    15:08:02.914768 IP 10.0.2.15.46318 > 10.0.2.3.domain: 9065+ PTR? 15.2.0.10.in-addr.arpa. (40)
            0x0000:  0004 0001 0006 0800 2788 0ca6 0000 0800  ........'.......
            0x0010:  4500 0044 c51a 4000 4011 5d7d 0a00 020f  E..D..@.@.]}....
            0x0020:  0a00 0203 b4ee 0035 0030 1853 2369 0100  .......5.0.S#i..
            0x0030:  0001 0000 0000 0000 0231 3501 3201 3002  .........15.2.0.
            0x0040:  3130 0769 6e2d 6164 6472 0461 7270 6100  10.in-addr.arpa.
            0x0050:  000c 0001                                ....
    5 packets captured
    10 packets received by filter
    0 packets dropped by kernel


    # 选择子网, net, src net, des net


    # 过滤协议，直接在后面写上协议名就好
    $ sudo tcpdump -i any -c 5 -n icmp
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    14:27:19.751355 IP 10.0.2.15 > 119.75.213.61: ICMP echo request, id 1369, seq 1, length 64
    14:27:19.760170 IP 119.75.213.61 > 10.0.2.15: ICMP echo reply, id 1369, seq 1, length 64
    14:27:20.752639 IP 10.0.2.15 > 119.75.213.61: ICMP echo request, id 1369, seq 2, length 64
    14:27:20.760858 IP 119.75.213.61 > 10.0.2.15: ICMP echo reply, id 1369, seq 2, length 64
    14:27:21.754795 IP 10.0.2.15 > 119.75.213.61: ICMP echo request, id 1369, seq 3, length 64
    5 packets captured
    5 packets received by filter
    0 packets dropped by kernel


    # 支持使用 and or 来表示符合的过滤条件
    $ sudo tcpdump -i any -c 5 -n "icmp and (port 80)"


    # 把捕获的包写入文件, -w
    $ sudo tcpdump -i any -c 10 -w debug.pcap

    # 读取刚刚写出的 debug.pcap 文件
    $ sudo tcpdump -r debug.pcap
    reading from file debug.pcap, link-type LINUX_SLL (Linux cooked)
    14:29:20.997275 IP 10.0.2.15.ssh > 10.0.2.2.64407: Flags [P.], seq 2565798981:2565799021, ack 21257223, win 22032, length 40
    14:29:20.997521 IP 10.0.2.2.64407 > 10.0.2.15.ssh: Flags [.], ack 40, win 65535, length 0
    14:29:21.005056 IP 127.0.0.1 > 10.0.2.15: ICMP echo reply, id 1369, seq 122, length 64
    14:29:21.005215 IP 10.0.2.15.44211 > 10.0.2.3.domain: 4253+ PTR? 61.213.75.119.in-addr.arpa. (44)
    14:29:21.013607 IP 10.0.2.3.domain > 10.0.2.15.44211: 4253*- 1/0/0 PTR 127.0.0.1. (67)


Reference
=========

- Introduction To TCPDUMP https://www.youtube.com/watch?v=hWc-ddF5g1I&list=WL&index=3