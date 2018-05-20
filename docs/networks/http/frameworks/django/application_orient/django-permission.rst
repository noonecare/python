===========
Recipe Name
===========

:Author: 王蒙
:Tags: Django, Web Frameworks, Python

:abstract:

    Django 权限控制

.. contents::

Audience
========

Python 开发，网站开发

Prerequisites
=============

python


Problem
=======

- 认证
- Model 级权限控制
- object 级权限控制
- view 级权限控制


Solution
========

- 认证

    django admin， django-brace 等都提供了认证用户的功能。


- model 级权限控制

    权限的控制粒度是整张表（而不是表中的记录）。django admin 是 django 提供的管理界面。django admin 就提供了 Model 级的权限控制。

- object 级权限控制

    表中不同的记录对同一用户的权限不同。django-guardian 提供了 object 级的权限控制。


- view 权限控制

    用户需要特定的权限才能执行 view, django-brace 提供了 access 级的权限控制。


Reference
=========

- Django By Example

