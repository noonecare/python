vagrant 和 docker 都是提供独立可执行环境的技术。docker 广泛用于部署，而 vagrant 仍然在开发中大量使用。


vagrant 最垃圾的地方是 box 太难下。基本下不下来。最后用迅雷下载，解决了问题。



win10 上 Docker 只能使用 Hyper-V 虚拟机启动， 开启了 Hyper-V 虚拟机之后， VirutalBox 不能正常使用。所以在 win10 上，虚拟机只能使用 Hyper-V。

进入 Hyper-V 虚拟机之后，发现不能访问互联网。按照 `Hyper-V 虚拟机无法上网的解决办法`_ 中的方法成功解决 Hyper-V 虚拟机不能访问互联网的问题。




Reference
==========

#. Hyper-V 虚拟机无法上网的解决办法 http://www.jb51.net/article/87827.htm