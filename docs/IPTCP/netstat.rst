================
netstat
================

:作者: 王蒙
:标签: 网络，TCP/IP，Linux/Unix

:简介:

    介绍 netstat 。

.. contents::

目标读者
==========

后端开发

预备知识
=============


问题
=======


解决办法
==========

踩过的坑
----------------

有个运行在 8080 端口的程序卡住了（不能接受新的连接），我想找到该进程的 pid, 然后重启该程序。于是我执行了

.. code-block:: shell

    $ sudo netstat -tp | grep 8080
    $

出现这个问题的原因是，默认 netstat 的输出结果中的 Local Address 列，会用进程名代替端口号。比如

.. code-block:: shell

    $ sudo netstat -tp
    Active Internet connections (w/o servers)
    Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
    tcp        0      0 10.201.80.86:38586      10.203.40.143:8433      ESTABLISHED 12040/./falcon-agen
    tcp        0      0 10.201.80.:zabbix-agent 10.201.80.105:49132     TIME_WAIT   -
    tcp        0      0 10.201.80.:zabbix-agent 10.201.80.105:60154     TIME_WAIT   -
    tcp        0      0 10.201.80.:zabbix-agent 10.201.80.105:50777     TIME_WAIT   -
    tcp        0      0 10.201.80.:zabbix-agent 10.201.80.105:59602     TIME_WAIT   -
    tcp        0      0 10.201.80.:zabbix-agent 10.201.80.105:50538     TIME_WAIT   -
    tcp        0      0 10.201.80.86:44702      10.201.50.10:4506       ESTABLISHED 2067/python

可以使用 -n 选项，强制所有的端口号都用数字表示。这样，就能找到运行在 8080 端口的进程。

.. code-block:: shell

    [wangmeng@gs-server-5389 ~]$ sudo netstat -tpn | grep 8080
    tcp        1      0 10.201.80.86:8080       10.202.233.70:62324     CLOSE_WAIT  -
    tcp        0      0 10.201.80.86:8080       10.202.234.238:62150    ESTABLISHED -
    tcp        0      0 10.201.80.86:8080       10.202.234.238:62152    ESTABLISHED -
    tcp        0      0 10.201.80.86:8080       10.202.234.238:62149    ESTABLISHED -
    tcp        0      0 10.201.80.86:8080       10.202.234.238:62151    ESTABLISHED -
    tcp        0      0 10.201.80.86:8080       10.202.234.238:62148    ESTABLISHED 19498/python
    tcp        0      0 10.201.80.86:8080       10.202.234.238:62153    ESTABLISHED -


参考文献
=========

- netstat命令: http://man.linuxde.net/netstat