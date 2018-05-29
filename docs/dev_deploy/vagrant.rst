===========
Vagrant
===========

:Author: 王蒙
:Tags: Python 开发，构建开发环境

:abstract:

    vagrant 能够方便地为开发提供虚拟执行环境。比如你使用 windows 的系统，但是开发必须基于 linux 环境（比如可能是因为某个 python 包只能运行在 linux 环境下）。这时候，可以方便地使用 vagrant 启动一个虚拟机来做开发。

.. contents::

Audience
========

Python 开发

Prerequisites
=============

docker


Problem
=======

- vagrant 和 docker 相比有哪些优势和劣势
- vagrant 基本使用方法
- 配置 VagrantFile 文件

Solution
========


vagrant 和 docker 相比有哪些优势和劣势？
---------------------------------------------------------------------


vagrant 用于提供开发环境，还是比 Docker 要方便一点：

    - Pycharm 使用 Vagrant 提供的 Python Interpreter， 代码能够自动补全。Pycharm 使用 Docker Interpreter 时，代码不能自动补全。
    - vagrant init 自动建立宿主机和虚拟机的目录对应关系，使得在虚拟机中直接就有当前工程的所有代码。如果使用 Docker 的话，需要自己去配置 Volume （配置目录对应关系）。
    - Pycharm 使用 Docker Interpreter 执行代码，每次都会创建，启动，停止 Docker Container， 这些步骤拖慢了程序的执行，影响了开发效率。Pycharm 使用 vagrant Interpreter 执行代码，就和在本地执行代码一样，没有任何 overhead(不必重启虚拟机)，所以速度比 Docker 快。

在部署方面，Docker 几乎完胜 vagrant。不过 vagrant 的虚拟机可以在 windows 操作系统上运行 linux 操作系统的虚拟机。但是 Docker 启动的 container 的操作系统内核必须和宿主机的操作系统内核大致相同。

在 Win10 操作系统下，要运行 docker 必须使用 Hyper-V ， 而使用了 Hyper-V 导致 VirtualBox 不能正常使用，导致 vagrant 必须也使用 Hyper-V。vagrant 使用 Hyper-V 特别别扭，完全抵消了 vagrant 带来的便利。所以在 Win10 下，在当前（未来可能有改进），还是采用 Docker 提供虚拟化的环境比较合适。

Vagrant 基本使用方法？
------------------------------------------------------------------------


- vagrant 最常用的命令

    .. code-block:: shell

        # 在工程的 root 目录下执行如下语句，会生成 VagrantFile 配置文件
        $ vagrant init {box_name}
        # 执行如下语句，会根据刚才生成的配置文件，启动一个虚拟机
        $ vagrant up
        # vagrant up 的时候，可以使用 Virtualbox 启动虚拟机，也可以使用 Hyper-V 启动虚拟机.
        # 执行如下语句，进入启动的虚拟机
        $ vagrant ssh

- 搜索 box, 下载 box, 把 box 添加到本地仓库

    可以到 `VagrantCloud`_ 搜索你需要的 box。

    理论上 vagrant init {box_name} 就能下载box， 但是实际在中国，下载 box 非常慢。我发现充了会员的迅雷，下载 vagrant box 非常快。你可以用迅雷先把 box 下载当本地。

    怎样把迅雷下载的 box 文件，添加到本地 box 仓库呢，请看下面的代码。

    .. code-block:: shell

        # 把保存在 {local_box_path} 的 box 添加到本地 box 仓库中，在本地 box 仓库中这个 box 的名为 {box_name} 。
        $ vagrant box add {box_name} {local_box_path}

        # 有了上一步你可以 执行 vagrant init  和 vagrant up 了。
        $ vagrant init {box_name}
        $ vagrant up


- Pycharm 使用 vagrant Interpreter

    Pycharm 可以在 settings -> python interpreter -> Add remote Interpreter 中选择使用 Vagrant Interpreter。
    Pycharm 能够根据 vagrant 虚拟机的 python 环境自动补全代码。比如虚拟机中安装了 pandas 包，那么在 pycharm 中写 import pa, pycharm 会自动提示要输入 ndas。



配置 VagrantFile 文件？
---------------------------------------------------------------------------------


vagrant init 命令生成的 VagrantFile 每行配置之前都有详细的注释，看注释就能明白这行配置是干什么的。

VagrantFile 中重要的配置有：

    - 同步目录（类似于 Docker 中的 Volume）

        .. code-block:: shell

            config.vm.synced_folder  "/Users/helei/www", "/vagrant"

    - 端口转发（类似于 Docker 中的 port）

        .. code-block:: shell

            config.vm.network :forwarded_port, guest: 80, host: 80

    - 是否能够访问互联网

        .. code-block:: shell

            # 不能访问互联网
            config.vm.network "private_network", ip: "192.168.33.10"
            # 能访问互联网
            #config.vm.network "public_network"

Reference
=========

- Pycharm Docker: https://www.jetbrains.com/help/pycharm/docker.html
- Pycharm Vagrant: https://www.jetbrains.com/help/pycharm/configuring-remote-interpreters-via-virtual-boxes.html#d31185e65
- vagrant 官方文档: https://www.vagrantup.com/docs/
- vagrant的配置文件vagrantfile详解: https://blog.csdn.net/hel12he/article/details/51089774


.. _VagrantCloud: https://app.vagrantup.com/boxes/search