=============
Django Model
=============

:读者: 王蒙
:标签: 网络编程，Web Framework

:简介:

    Model 使得 Django 操作数据库变得非常简单。

.. contents::

目标读者
========

Python 开发，网站开发

预备知识
=============

Python, ORM


问题
=======

- Model 带来了那些好处？
- Model 的使用：

    - Model 定义
    - django migrate
    - Model 增删改查
    - Model 和 ModelAdmin
    - 自定义字段
    - Model 继承
        - Multi
        - Proxy
        - Abstract

    - 优化查询效率

解决办法
========

Model 带来了那些好处？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 很容易改用别的数据库去实现。比如代码之前使用 mysql, 后来想改用 postgesql , 只要去 settings.py 文件中修改配置即可。
- Model 建立了数据库记录与对象的映射，使得可以使用处理对象的方式处理数据库，特别是在处理外键的时候非常方便。
- Model 提供了很多抽象层次很高的字段，比如 EmailField 会自动确保输入的字符串是符合邮箱格式的字符串。除此之外，还可以自定义字段。
- Model 提供了很多非常简洁的筛选过滤的操作。

Model 的使用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Model 的定义
^^^^^^^^^^^^^^^^^

- 给出该 Model 需要的字段。
- Django 提供了丰富的字段（比数据库提供的字段要丰富，比如提供了 FileField 等字段）。Django 有哪些字段请参考 `Model Field Reference`_ 。
- 注意 relationship fields 字段。
- Model 中的嵌套类 class Meta 定义了该 Model 的 metadata。具体参考 `Model meta options`_ 。举个例子：class Meta: ordering = ('title', '-created') 表示查询结果以 title 升序， created 降序排列。


- Model class Meta 中要特别注意 Model 的三种**继承模式**。


- Abstract: 被继承的 Model, 不会建立对应的表。继承的 Model 会在被继承 Model 的基础上添加字段。

    .. code-block:: python

        from django.db import models
            class BaseContent(models.Model):
            title = models.CharField(max_length=100)
            created = models.DateTimeField(auto_now_add=True)
            class Meta:
                # abstract inherit
                abstract = True

        class Text(BaseContent):
            body = models.TextField()

- Multi-table： 被继承的 Model, 也会建立对应的表。继承的 Model 会在被继承 Model 的基础上添加字段。

    .. code-block:: python

        from django.db import models
        class BaseContent(models.Model):
            title = models.CharField(max_length=100)
            created = models.DateTimeField(auto_now_add=True)

        class Text(BaseContent):
            body = models.TextField()

- Proxy：被继承的 Model 会建立对应的表，但是继承的 Model 对应的表就是被继承 Model 的表。继承的 Model 是添加了新的方法（不更改字段），方便使用。

    .. code-block:: python

        from django.db import models
        from django.utils import timezone
        class BaseContent(models.Model):
            title = models.CharField(max_length=100)
            created = models.DateTimeField(auto_now_add=True)


        class OrderedContent(BaseContent):
            class Meta:
                proxy = True
                ordering = ['created']

            def created_delta(self):
                return timezone.now() - self.created



在数据库中创建 model 对应的数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


下面两句命令，会在数据库中创建以及更新 model 对应的数据：

        $ python manage.py makemigrations {app_name}
        $ python manage.py migrate


Model 的增删改查
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

增加记录

    .. code-block:: python

        # 新建 model 时，注意一点，就是外键取值是个对象，不是键值
        m = Module(course=course, title='title', description='description')
        # 不执行 save 不会把该对象保存到数据库中
        m.save()

        # Model manager 的 create 方法也能新建对象。而且 create 创建对象，不必再调用 save 方法。
        Module.objects.create(title='title', description='description')

删除记录：

.. code-block:: python

        # m is an instance of a kind of Model.
        m.delete()

        # 批量删除一批
        User.objects().all().delete()


更新记录：

.. code-block:: python

        # m is an instance of a kind of Model.
        m.title = 'change_title'
        # you have to call save method, to update change to database.
        m.save()

- 查询，Django 查询需要了解 QuerySet , 详细的 QuerySet API, 参见 `Make Query`_ 。

        - 双下划线查询字段。
        - Q 函数，组合查询条件。
        - F 函数，选择自身的字段。
        - aggregate 聚合查询，annotate per-object 聚合查询。


自定义字段
~~~~~~~~~~~~~~~~~~

Django model 可以自定义字段，下面是个自定义字段的例子。更多内容查看 `custom-model-fields`_ 。

    .. code-block:: python

        class OrderField(models.PositiveIntegerField):

            def __init__(self, for_fields=None, *args, **kwargs):
                self.for_fields = for_fields
                super(OrderField, self).__init__(*args, **kwargs)

            def pre_save(self, model_instance, add):
                if getattr(model_instance, self.attname) is None:
                    # no current value
                    try:
                        qs = self.model.objects.all()
                        if self.for_fields:
                            # filter by objects with the same field values for the fields in "for_fields"
                            query = {field: getattr(model_instance, field) for field in self.for_fields}
                            qs = qs.filter(**query)
                        # get the order of the last item
                        last_item = qs.latest(self.attname)
                        value = last_item.order + 1
                    except ObjectDoesNotExist:
                        value = 0
                    setattr(model_instance, self.attname, value)
                    return value
                else:
                    return super(OrderField, self).pre_save(model_instance, add)

ModelAdmin
~~~~~~~~~~~~~

Django 自身提供了 Admin 管理界面。ModelAdmin 定义了 Model 在 Admin 管理界面如何展示。

    .. code-block:: python

        class PostAdmin(admin.ModelAdmin):
            list_display = ('title', 'slug', 'author', 'publish', 'status')
            list_filter = ('status', 'created', 'publish', 'author')
            search_fields = ('title', 'body')
            prepopulated_fields = {'slug': ('title', )}
            raw_id_fields = ('author',)
            date_hierarchy = 'publish'
            ordering = ['status', 'publish']

        admin.site.register(Post, PostAdmin)


优化查询效率
~~~~~~~~~~~~~~

Django 中 QuerySet 负责实际查询数据库（把ORM访问方式翻译成 SQL 语句，访问数据库）。QuerySet 是 lazy evaluated（延迟计算的，只有到实际用的时候才会运算）。除此之外 QuerySet 在某些条件会下缓存查询结果，尽可能多地使用缓存的结果，少访问数据库，是可以提高效率的。
下面举例说明几个提高查询效率的细节：


        lazy evaluated： QuerySet 是 lazy evaluated。如下代码其实就访问了数据库一次，是 print 触发了数据访问。

        .. code-block:: python

                q = Entry.objects.filter(headline__startswith="What")
                q = q.filter(pub_date__lte=datetime.date.today())
                q = q.exclude(body_text__icontains="food")
                print(q)

         特别注意，外键也是 lazy evaluated。就是说 QuerySet 首先获得外键的键值（id 号），到真需要外键对应的对象时，才会查询数据库得到外键对应的对象。

        比如对于如下代码，只有到 print(b.a) 才会访问数据库，得到 a instance 。

        .. code-block::

                class A(models.Model):
                        foo = models.IntegerField()

                class B(models.Model):
                        a = models.ForeignKey(A, on_delete=models.CASCADE, related_name="bs")


                b = B.objects.first()
                print(b.a_id)
                print(b.a)




        select_related：是针对 ForeignKey 和 OneToOne 字段的优化。比如

        .. code-block:: python

                actions = actions.filter(user_id__in=following_ids)
                                .select_related('user', 'user__profile')



        .. code-block:: python

                actions = actions.filter(user_id__in=following_ids)

                for action in actions:
                        # action.user 会执行一次 SQL 查询，多次执行会使性能变差。
                        user = action.user
                        # user.profile 会执行一次 SQL 查询，多次执行会使性能变差。
                        user_profile = user.profile

        select_related 的优势在于，把多次数据库查询整成了一次数据库查询（通过 SQL 中的 join 完成），提高了效率。

        select_related 用于 ForeignKey 和 OneToOne 字段。



        prefetch_related:

                prefetch_related 用户 ManyToMany 字段和反向 ForeignKey 关系。

                prefetch_related 能提高性能的原因在于会缓存查询结果，减少数据库访问次数。

                以 https://docs.djangoproject.com/zh-hans/2.0/ref/models/querysets/#prefetch-related 中的例子为例。


                prefetch_related 会提交执行 Toppings.objects.all() ，把所有的 toppings 缓存到本地。然后用 Python 对每个 Pizza instance 和 toppings 做 join。得到每个 Pizza instance 对应的 toppings 。

                todo: 我常常想，如果数据库比较大，prefetch_related 会不会导致内存错误。

                .. code-block:: python

                        Pizza.objects.all().prefetch_related('toppings')


Manager
~~~~~~~~~~~~~

manager 是访问 Model 的接口。每个 Model 至少有一个 manager。

继承 `models.Manager` 类，重写 get_queryset 方法，返回 QuerySet 就能自定义 manager。

objects 是 Model 的默认的 manager。

我认为自定义 manager，主要为了少写代码。比如很多 sql 都需要做某些过滤操作，那么可以把这些过滤操作放到自定义 manager 中，使用该自定义 manager， 就相当于预先做了过滤。




参考文献
=========

- Django by Example.
- Django 中的 select_related 与 prefetch_related: http://baijiahao.baidu.com/s?id=1589827357928613968
- Aggregation: https://docs.djangoproject.com/en/2.0/topics/db/aggregation/
- When QuerySets are evaluated: https://docs.djangoproject.com/en/2.0/ref/models/querysets/#when-querysets-are-evaluated
- Model Field Reference: https://docs.djangoproject.com/en/2.0/ref/models/fields/
- Make Query: https://docs.djangoproject.com/en/2.0/topics/db/queries/
- custom model fields: https://docs.djangoproject.com/en/2.0/howto/custom-model-fields/

.. _Model Field Reference: https://docs.djangoproject.com/en/2.0/ref/models/fields/
.. _Model meta options: https://docs.djangoproject.com/en/2.0/ref/models/options/
.. _Make Query: https://docs.djangoproject.com/en/2.0/topics/db/queries/
.. _custom-model-fields: https://docs.djangoproject.com/en/2.0/howto/custom-model-fields/