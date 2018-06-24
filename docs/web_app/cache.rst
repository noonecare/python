===========
Cache
===========

:作者: 王蒙
:标签: 软件开发，网络编程

:简介:

    缓存是广泛使用的提高效率的工具。那么如何设计缓存，如何使用使用缓存呢？这个小节，总结我知道的缓存技术。

.. contents::

目标读者
========

软件开发，网络编程

预备知识
=============

Python, 算法分析与设计

问题
=======

缓存的应用

缓存的工具

分布式缓存


解决办法
========

- 缓存的应用

    - Memorization Algorithm（动态规划）算法用内存空间换时间，缓存反复使用的中间结果提高计算的效率。
    - 数据库中，缓存常用的查询结果。提高查询效率。
    - CDN 缓存，把资源缓存到离客户近的位置，提高客户访问资源的效率。

    缓存的关键指标是 **命中率** 。

    Djnago 使用缓存特别简单，参见 `Django’s cache framework`_ 学习如何在 Django 中使用缓存。

- 缓存的工具

    - 可以使用内存做缓存。python 的 `functools.lru_cache` 提供了简便地把数据缓存到内存中的功能。（重点）
    - 缓存服务（重点），特别要注意缓存可以设过期时间。

        - memcached
        - redis

    - 知道，却从未用过的缓存工具：

        - Varnish


- 分布式缓存

    分布式缓存最大的问题，就是尽可能地均分缓存任务，避免出现缓存热点（Hot Spot）影响性能。

    哈希槽（hash slot）算法：

        - 根据缓存 key 的 hash 值，把缓存分配到多台缓存服务器上。

        - 读取缓存时，根据缓存 key 的 hash 值，访问响应的缓存服务器得到缓存的值。

        - 当需要添加或者删除缓存服务器时，需要做大量的数据迁移工作，很费事儿。一致性哈希算法解决了这个问题。

    一致性哈希算法（consistent hashing）：

        添加缓存服务器，只要迁移添加的缓存服务器之后（顺时针旋转的后面）的第一台服务器中的部分缓存到新添加的缓存服务器即可。

        我认为 redis 集群应该已经实现了一致性哈希算法，实际参考 `从一致性哈希算法到缓存集群实现`_ 发现确实如此。这样的话，开发网站时，一般不用自己去实现一致性哈希算法。




参考文献
=========

- Varnish: https://github.com/varnishcache/varnish-cache/
- 从一致性哈希算法到缓存集群实现: https://zhuanlan.zhihu.com/p/34293054
- python redis:
- Django By Example Chapter 11 Caching Content.

.. _Django’s cache framework: https://docs.djangoproject.com/en/dev/topics/cache/