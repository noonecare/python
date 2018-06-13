===========
Restful
===========

:作者: 王蒙
:标签: 网络编程

:简介:

    Restful 是种软件设计风格。

.. contents::

目标读者
========

网络编程，微服务

准备知识
=============


问题
=======

- 为什么需要 Restful

- Restful 风格的要求

- 最佳实践


解决办法
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



- 最佳实践

    - URI 用名词命名，不要用动词命名。比如你要做删除的动作，不要写成 GET /someresouce/delete， 应该写成 DELETE /someresource 。
    - 所有的动作使用 HTTP METHOD 实现。
    - GET, HEAD METHOD 不要对资源做任何修改。
    - 修改资源使用 POST, PUT, DELETE 等操作。
    - 新建资源使用 POST 不要使用 PUT。
    - PUT 方法要求是幂等的，POST 一般不是幂等的。
    - 表示资源集合的URI采用复数。常见的 Restful API 几乎表示资源集合都采用复数。表示资源集合中具体某一个资源，直接使用 /id 的表示。比如 /someresources/1 。
    - 出错时，Restful API 返回的响应中，应当包含 body, 该 body 一定要记录错误的信息（比如记录错误的原因，错误类型，错误发生在哪里等），一般 body 中也会包含错误码。Restful API 返回的响应的状态码以及响应的 body 中包含的错误码都应该采用 HTTP 协议规定的错误码，不要自定义错误码。
    - API 版本可以放在 header 中，也可以放在资源 URL 之前。如果资源有嵌套，请放在具体的资源之前，不要放在 URL 的根路径之前。
    - 尊重 HTTP 返回码规范，不要自定义返回码。常见的返回码，以及返回码的含义如下：

        - 2XX 表示成功
        - 3XX 表示重定向
        - 4XX 表示客户端错误
        - 5XX 表示服务器端错误
        - 200 ok
        - 301 永久重定向
        - 302 临时重定向
        - 304 缓存资源没有改变
        - 401 未认证
        - 403 没有权限
        - 404 找不到资源


- 优秀 RestAPI 范例


- 我踩过的坑

    - 资源集合没有用复数。
    - 自定义了错误码。
    - 使用 PUT 创建资源。
    - API 版本号放在 URL 末尾。



参考文献
=========

- 见到的另一篇讲解Restful不错的文章： https://blog.csdn.net/fengxinziyangyang/article/details/51459299
- Representational State Transfer (REST)： http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
- 重新解析REST Service： https://blog.csdn.net/zhoudaxia/article/details/16716403
- RESTful API 设计指南: http://www.ruanyifeng.com/blog/2014/05/restful_api.html
- 《HTTP 权威指南》 Status Codes 61 页
.. _重新解析REST Service: https://blog.csdn.net/zhoudaxia/article/details/16716403