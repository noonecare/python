===========
postgresql
===========

:作者: 王蒙
:标签: 数据库，postgresql

:简介:



.. contents::

目标读者
========

后端开发

预备知识
=============

Standard SQL

问题
=======

Postgresql 的特点


解决办法
========

- use database

    根据[stackoverflow](https://stackoverflow.com/questions/10335561/use-database-name-command-in-postgresql), 可知 postgresql 只有重新建立与数据库的连接，才能切换数据库。

- 在 postgresql 中单引号和双引号

    postgresql中字符串需要用单引号包裹，如果使用双引号，系统将认为那是变量。


参考文献
=========
