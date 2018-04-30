Python 发布应用：

    #. 以脚本发布，适用于较小的项目
    #. 以 Python 安装包发布
    #. 以 X As a Service 的方式，发布服务

本章主要讲了以 X as a Service 的方式发布应用。

The Twelve-Factor App
=====================

开发易用部署 App 的 12 个关键要素

#. codebase：有且只有一个 codebase（可以有两个 codebase，一个写包，一个写具体部署的应用，比如引用包，且把配置文件填好。）
#. backend service:
#. log:
#. config：Store config in the environment.
#. Dependencies: 明确写出依赖。
#. Disposability: 快速开启，优雅退出
#. Admin process: Run admin/management tasks as one-off process.
#. Build, release, run: 严格区分构建和运行
#. Process: 以一个或多个无状态的进程运行程序
#. Concurrency: 易于扩展
#. Porting Binding: 易于更改端口号
#.



Deploying automation using Fabric
=================================

`Fabric`_ 是很流行的 Python 自动部署工具。能够完成把代码远程到多台服务器的功能。Fabric 能够方便地执行 shell 命令，能够通过
ssh 在远程执行 shell 名。 Fabric 还能实现交互式的输入密码验证的功能。Fabric 中 run 和 local 是其中最重要的函数。


Your own package index or index mirror
======================================


PyPI mirroring
--------------

应该在公司级别搭建自己的 PyPI，Python 官方 PyPI 的 Availability 是没有保证的。

有很多工具搭建私有的 PyPI, 《expert python programming》 推荐使用 `devpi`_ 。这个工具相对于其他工具的好处在于：

* 能够缓存你需要的 Python 官方 PyPI 包。
* 能够周期更新你需要的 Python 官方 PyPI 包。

其他的搭建 PyPI 工具，要不不同步 Python 官方 PyPI 包，要不就是全备份导致磁盘占用特别高。相对来说 devpi 提供了 Python 官方 PyPI
包，同时又不占用过多的资源，唯一的确定就是 devpi 包提供的官方 PyPI 包可能不是最新的。


Deploying use package
---------------------

setup.py 中能够自定义操作，这些操作可用于自动化部署应用。这些步骤一般会在开发环境执行。

MANIFEST.in 可以用于 bundle 很多文件，比如 SASS 或者 LESS 等等。



Common conventions and practices
--------------------------------

The filesystem hierarchy
^^^^^^^^^^^^^^^^^^^^^^^^

* Choose wisely and avoid surprises
* Be Consistent across all the available infrastructure of your project
* Try to be consistent across your organization

有了 setup.py ，project 的目录结构可以写的很多样化，不管怎么样都能打包。不过一定要注意保持一致性。

Isolation
^^^^^^^^^

建立独立的运行环境来开发。对于系统有太多依赖，在部署的时候，可能会出现很多问题。

Using process supervision tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using nohup, screen, or tmux to semi-daemonize the process is not an option. Doing so is like designing your service to
fail.

What you need is to have some process supervision tool that can start and manage your application process.  Before
Choosing the right one you need to make sure it:

* Restarts the service if if quits.
* Reliably tracks its state
* Captures its stdout/stderr streams for logging purposes
* Runs a process with specific user/group permissions
* Configures system environment variables


**init.d**, **upstart**, **runit** 不合适，因为它们不是给用户级别的应用设计的，而且非常难以维护。

在 Python 中，常用 `Supervisor`_ 和 `Circus`_ 来管理用户应用。 Supervisor 暂时不支持 Python3, 所以可以使用 Circus。


Application code should be run in user space.
--------------------------------------------

貌似常常用和应用同名的用户，执行应用。

绝对不要以超级用户权限部署应用，那样的话，应用之间可能会相互影响。


Using reverse HTTP proxy
------------------------


使用反响代理的好处有：

* TLS/SSL 一般会由 nginx 来做，降低了应用的复杂性。
* 应用一般不会使用super user 权限执行，但是反向代理可以。HTTP 一般服务于 80 端口，HTTPS 一般服务于 HTTPS 端口。普通用户
  没有权限绑定 80/443 端口。但是超级用户有权限。
* Nginx 能更高效地提供静态文件。
* Nginx 可以伪装出多个 host。DNS 中一个 IP 可以对应多个域名。nginx 服务器中 每个 server 通过 server_name 选项匹配域名，
  这样就实现了一台主机用多个域名，提供多种服务的功能。
* nginx 可以提供缓存和负载均衡的功能。

其实这些好处，就是 nginx 常见的应用。


Reloading processes gracefully
------------------------------

好奇这种方式具体是怎么实现的，先看看 gunicorn 处理信号的源码。

#. 当接到 TERM 信号时，应用应该停止接受新的请求，并且处理完所有已经接受的请求，然后退出。
#. 当接到 HUP 信号时，应用久的节点优雅退出（不再接受请求，但是会处理已经接受到的请求），新的节点（worker）应该开始接受新
的请求，确保服务没有间断。
#. Python 中的 `Gunicorn`_ 和 `uWSGI`_ 都支持不间断服务的重载方式。可以参考这两个框架的做法设计自己的应用。



Code instrumentation and monitoring
-----------------------------------


#. 查看日志，比如不同返回码的日志有多少条。
#. 错误日志和警告日志。
#. 资源占用（比如 CPU, memory 和带宽等）。
#. 和商业价值有关的指标（客户占有率，投资回报等）。


Logging Errors
^^^^^^^^^^^^^^

不管程序写得多完美，都保不齐会发生错误。What you can do is be well prepared for such scenarios and make sure no error
passes unnoticed.

网络应用的错误，一般对应错误报错日志或者警告。所以如何从日志中发现问题，显得非常重要。处理把日志记录的尽可能规范之外，使
用日志处理工具也很重要。

Sentry 是 Python 中搜集错误日志，系统崩溃报告最有名的工具。

Sentry 软件是开源的，你可以自己维护 Sentry 服务，也可以选择付费使用 Sentry 服务（那样就不用自己去维护）。

DSN: 我去 Sentry 官网注册了个号，然后建立了一个 project, 于是 Sentry 给了我一个 DSN(https://13c5b7dbdb544a7ea37177997fbc8e66:d68d511723e147f4bbdb132af22f04aa@sentry.io/1197614)。
有了这个 DSN 我可以把出错日志写到 Sentry 中。我很简单的使用了下 Sentry, 给我的感觉是有很多有用的信息，比如有 Stacktrace
会把出错的哪一行代码标出来。除此之外，还会显示是那台主机，用的那个版本的 Python，什么时候发生的错误等等信息。除此之外
Sentry 界面很友好。最后 Sentry 可以很容易的集成到很多语言，框架中。

比如对于 Python。Sentry 提供了 raven 包。python 装上这个包之后，很容易与 Sentry 集成。具体的参见 `Python Sentry Document`_ 。

Monitoring system and application metrics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


monitor performance 的工具非常多。比较常用的有:

#. Munin
#. StatsD
#. Graphite


Dealing with application logs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

logs are not only about errors.


Tools for log process
^^^^^^^^^^^^^^^^^^^^^


.. _Circus:
.. _Supervisor:
.. _Gunicorn:
.. _uWSGI:
.. _Python Sentry Document: https://docs.sentry.io/clients/python/


.. _Fabric: http://www.fabfile.org
.. _devpi: https://devpi.net/docs/devpi/devpi/stable/%2Bd/index.html
