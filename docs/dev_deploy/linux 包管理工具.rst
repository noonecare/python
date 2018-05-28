===================
linux 包管理工具
===================

:Author: 王蒙
:Tags: linux, DevOps, Docker, Vagrant, yum, apt-get

:abstract:

    介绍 linux 上的 yum 和 apt-get 装包工具。

.. contents::

Audience
========

DevOps

Prerequisites
=============

简单的 bash 命令，Docker

Problem
=======

- 安装源
- 常用命令
- 在 Docker 如何使用


Solution
========

- 安装源

    为了提高下载包的速度，需要更换为国内源。

        - `把 yum 源改成是国内源`_
        - `debian系linux，更换apt-get官方源为国内源`_




- 常用命令

    yum
        - yum makecache

            缓存源服务器的包信息（都有哪些包，包依赖关系）到本地。之后查询，查询的是本地缓存的包信息；安装时，也会查询本地缓存的包信息，可能会出现源服务器有某个包，本地缓存没有的情况。

        - yum upgrade, yum update

            根据本地缓存的包信息，更新所有已安装的包。yum upgrade 和 yum update 的功能几乎一样，推荐使用 yum upgrade。


        - yum clean

            下载的 rpm 会占磁盘，清理这些 rpm 安装包，使用 yum clean 命令。

        - yum install

            安装 rpm 包。

        - \-y

            yum install, yum upgrade, yum update 时，可能会弹出对话框，需要填 yes/no 才能继续操作。\-y 的意思就是一路 yes，使得安装过程不需要交互。\-y 在 Dockerfile 经常用。

    apt-get

        - apt-get update

            缓存服务器的包信息，并根据缓存的包信息，更新已安装的包。

        - apt-get install

            装包

        - \-y

            一路 yes, 使得安装过程不需要交互。\-y 在 Dockerfile 中经常用。


- 在 Dockerfile 中如何使用

    Dockerfile 使用 \-y 选项（比如 apt-get -y install, apt-get -y update, yum -y upgrade, yum -y install ），使得安装过程不需要交互。



Reference
=========

- 把 yum 源改成是国内源: https://blog.csdn.net/inslow/article/details/54177191
- debian系linux，更换apt-get官方源为国内源: https://blog.csdn.net/yjk13703623757/article/details/78943345


.. _把 yum 源改成是国内源: https://blog.csdn.net/inslow/article/details/54177191
.. _debian系linux，更换apt-get官方源为国内源: https://blog.csdn.net/yjk13703623757/article/details/78943345