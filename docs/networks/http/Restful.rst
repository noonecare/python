===========
Restful
===========

:Author: 王蒙
:Tags: 网络编程

:abstract:

    Restful 是种软件设计风格。

.. contents::

Audience
========

网络编程，微服务

Prerequisites
=============


Problem
=======

- 为什么需要 Restful

- Restful 风格的要求

- Restful best practice


Solution
========

- 为什么需要 Restful

    当前开发需要多人协作，有效的沟通需要一套规范（解耦前端开发和后端开发）。Restful 接口就是这样一套规范。

    开发时，把一切数据，服务等等统统看成 Resource。使用 URI 定位 Resource，使用 METHOD 描述操作。力求做到

        - 看 Url 就知道要什么
        - 看 http method 就知道干什么
        - 看 http status code 就知道结果如何


    （这些是我从下面的参考文献中抄的，我认为言简意赅，写的非常好）


- Restful 风格要求

    Fielding 的论文中写到 Restful 要求：
        • Identification of resources
        • Manipulation of resources through representations
        • Self-descriptive messages
        • Hypermedia as the engine of application state


    上面四句话太抽象。我看了 `重新解析REST Service`_ 才明白这四句话的意思。



- Rest Best Practice

    - URI 用名词命名，不要用动词命名。比如你要做删除的动作，不要写成 GET /someresouce/delete， 应该写成 DELETE /someresource 。
    - 所有的动作使用 METHOD 实现。
    - GET, HEAD METHOD 不要对资源做任何修改。
    - 修改资源使用 POST, DELETE 等操作。


Reference
=========

- 见到的另一篇讲解Restful不错的文章： https://blog.csdn.net/fengxinziyangyang/article/details/51459299
- Representational State Transfer (REST)： http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
- 重新解析REST Service： https://blog.csdn.net/zhoudaxia/article/details/16716403


.. _重新解析REST Service: https://blog.csdn.net/zhoudaxia/article/details/16716403