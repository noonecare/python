===========
ORM
===========

:Author: 王蒙
:Tags: 网络开发，数据库，ORM

:abstract:

    介绍 Python 以 ORM 操作数据库的方式。

.. contents::

Audience
========

Python 开发

Prerequisites
=============

数据库基本操作

Problem
=======

- SQLAlchemy
- Django ORM

Solution
========


Django Model 在介绍 Django 时有论述。这里重点介绍 SQLAlchemy。


SQLAlchemy 与数据库交互有以下两种方式：

- 使用 `SQL Statements and Expressions API`_

    SQLAlchemy 用这套 API 构建出 SQL 语句，交给 Connection 执行。

    参考 `代码`_，学习使用 SQLAlchemy SQL Statements and Expression API 方式与数据库交互。

    SQLAlchemy 直接使用 SQL 语句查询数据库。

- `ORM`_

    - 参考 `使用 SQLAlchemy`_ 快速上手 SQLAlchemy ORM 使用方式。

    - 使用过程中，我认为 ORM 处理外键（relation）的方式，让编程变得简单。使用 relation 时，有一点不方便，就是

        # 传给 relationship 的第一个参数是类名字符串（注意不是表名），如果以后可以直接传入类，在重构代码时，会比现在方便很多。
        books = relationship('Book')

        我使用 relationship 时，一般会加上 backref 参数。这样，在另一张表中，也可以用 . 访问属性的方式，访问外键。

        members = relationship('OrganizeStructure', backref=backref('group'))

    - 按照 `PEP 249`_ 要执行 commit，才会把数据写入数据库。


创建 Connection

SQLAlchemy 提供了 `MetaData`, `engine` 和 `Session` 来创建连接。MetaData 代表数据库

    创建 Metadata:

        .. code-block:: python

            from sqlalchemy import MetaData

            metadata = MetaData()


        .. code-block:: python

            from sqlalchemy.ext.declarative import declarative_base
            # 在 ORM 中使用，该 Base 除了代表数据库之外，还会进行 ORM 变换。
            Base = declarative_base()



    创建表

        .. code-block:: python

            # 创建表
            metadata.create_all(engine)


        .. code-block:: python

            # 在 ORM 中创建表
            Base.metadata.create_all(engine)

    创建 engine

        这是 SQLAlchemy 非常方便的点。要更改数据库，比如要从 postgresql 改成 mysql, 改下 engine 就可以了。

        还有就是测试的时候，使用 memory 数据库会非常方便（这样做测试的时候，不需要启动外部数据库，使得测试流程完全自动化）。下面的代码就创建了 memory 数据库 engine。

        .. code-block:: python

            from sqlalchemy import create_engine

            engine = create_engine('sqlite:///:memory:', echo=False)



    创建 connection 和 session

        使用 ORM 方式需要创建 session

            .. code-block:: python

                session = Session(bind=engine)

        使用 SQL Statements and Expressions API 方式，需要创建 Connection。

            .. code-block:: python

                session = engine.connect()


Transaction

    `SQLAlchemy Transaction`_
    `SQLAlchemy Transaction official document`_

    Transaction 就是一系列的 SQL 操作，这一系列操作要不全部执行成功，要不一个也不成功。SQLAlchemy 通过 `rollback()` 来实现 Transaction。
    常见的使用方式如下

    .. code-block:: python

        transaction = connection.begin()
        try:

            # 一系列操作

        except IntegrityError as e:
            # 出现错误，把数据库状态整回一系列 SQL 操作之前
            transaction.rollback()

    有的 engine（数据库）不支持在 connection 中指定 save_point（rollback() 回到的状态），如何设 save_point 查看上面提到的文档。

todo: 看完 https://github.com/oreillymedia/essential-sqlalchemy-2e 的代码。


Reference
=========

- PEP 249: https://www.python.org/dev/peps/pep-0249/
- SQLAlchemy Document: http://docs.sqlalchemy.org/en/latest/
- essential SQLAlchemy
- essential SQLAlchemy 源码: https://github.com/oreillymedia/essential-sqlalchemy-2e


.. _SQLAlchemy Transaction: http://www.codexiu.cn/python/sqlalchemy%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B/531/
.. _SQLAlchemy Transaction official document: http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html
.. _使用 SQLAlchemy: https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0014021031294178f993c85204e4d1b81ab032070641ce5000
.. _SQL Statements and Expressions API: http://docs.sqlalchemy.org/en/latest/core/expression_api.html
.. _代码: https://github.com/oreillymedia/essential-sqlalchemy-2e/tree/master/ch04
.. _PEP 249: https://www.python.org/dev/peps/pep-0249/
.. _ORM: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html