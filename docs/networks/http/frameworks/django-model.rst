=============
Django Model
=============

:Author: 王蒙
:Tags: 网络编程，Web Framework

:abstract:

    Model 使得 Django 操作数据库变得非常简单。

.. contents::

Audience
========

Python 开发，网站开发

Prerequisites
=============

Python, ORM


Problem
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

Solution
========

- Model 带来了那些好处？

    - 很容易改用别的数据库去实现。比如代码之前使用 mysql, 后来想改用 postgesql , 只要去 settings.py 文件中修改配置即可。
    - Model 提供了很多抽象层次很高的字段，比如 EmailField 会自动确保输入的字符串是符合邮箱格式的字符串。除此之外，还可以自定义字段。
    - Model 建立了数据库记录与对象的映射，使得可以使用处理对象的方式处理数据库，特别是在处理外键和连接的时候非常方便。

- Model 的使用

    - Model 的定义

        - 写出该表需要的字段。
        - 特别注意下外键的定义， 比如 Course 类下的 owner = models.ForeignKey(User, related_name='courses_created')， 表示 Courser 类通过 owner 外键连接到 User 表。 在程序中使用时， courser.owner 直接就是 User 类的实例。related_name='courses_created' 表在在 User 字段中用 courses_created 属性表示连接到该 User 的所有 Course。
        - Django 定义外键的方式和 SQLAlchemy 不同。我觉得 Django Model 的定义方式更简洁流畅。
        - class Meta: ordering = ('title', '-created') 用于表示查询结果以 title 升序， created 降序排列。

        .. code-block::

            class Post(models.Model):
                STATUS_CHOICES = (
                        ('draft', 'Draft'),
                        ('published', 'Published'),
                        )
                title = models.CharField(max_length=250)
                slug = models.SlugField(max_length=250, unique_for_date="publish")
                author = models.ForeignKey(User, related_name='blog_posts')
                body = models.TextField()
                publish = models.DateTimeField(default=timezone.now)
                created = models.DateTimeField(auto_now_add=True)
                updated = models.DateTimeField(auto_now=True)
                status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

                objects = models.Manager()
                published = PublishedManager()


                class Meta:
                    ordering = ('-publish', )

                def __str__(self):
                    return self.title

                def get_absolute_url(self):
                    return reverse('blog:post_detail', args=[self.publish.year,
                        self.publish.strftime('%m'),
                        self.publish.strftime('%d'),
                        self.slug])

    - django migrate

        {app_name} app 更改（包括新建）了 models, 执行如下两句命令，更新数据库。

        $ python manage.py makemigrations {app_name}
        $ python manage.py migrate


    - Model 的增删改查

        - 增加记录，就是新建 Model 对象，然后执行 save() 方法保存，比如：

            .. code-block::

                # 新建 model 时，注意一点，就是外键取值是个对象，不是键值
                m = Module(course=course, title='title', description='description')
                m.save()

                # Model manager 的 create 方法也能新建对象。
                Module.objects.create(title='title', description='description')

        - 删除记录，就是找到 Model 对象，然后执行 delete() 方法删除，比如：

            .. code-block::

                # m is an instance of a kind of Model.
                m.delete()

        - 改写，就是直接给 Model 对象的属性值赋值。比如：

            .. code-block::

                # m is an instance of a kind of Model.
                m.title = 'change_title'
                # you have to call save method, to update change to database.
                m.save()

        - 查询，Django Model 查询返回的结果是 **QuerySet** ， QuerySet 是 lazily evaluated 的。Django Model 使用 \_\_ 解析字段取值的方式很特别。

            .. code-block::

                # get all modules.
                all_posts = Post.objects.all()

                # filter() method.
                Post.filter(publish__year=2015, author__username='admin')
                # exclude() method.
                Post.objects.filter(publish__year=2015).exclude(title_startswith='Why')
                # order_by() method.
                Post.objects.order_by('title')
                # Ascending order is implied, you can indicate descending order with a negative sign prefix, like this:
                Post.objects.order_by('-title')

                # Post.objects is the Manager for Post Model, you can define your own Manager. e.g.

                class PublishedManager(models.Manager):
                    def get_queryset(self):
                    return super(PublishedManager,
                    self).get_queryset()\
                    .filter(status='published')

                class Post(models.Model):
                    # ...
                    objects = models.Manager() # The default manager.
                    published = PublishedManager() # Our custom manager.

- Model 和 ModelAdmin

    Django 自身提供了 Admin 管理界面。ModelAdmin 定义了 Model 在 Admin 管理界面如何展示。


    .. code-block::

        class PostAdmin(admin.ModelAdmin):
            list_display = ('title', 'slug', 'author', 'publish', 'status')
            list_filter = ('status', 'created', 'publish', 'author')
            search_fields = ('title', 'body')
            prepopulated_fields = {'slug': ('title', )}
            raw_id_fields = ('author',)
            date_hierarchy = 'publish'
            ordering = ['status', 'publish']

        admin.site.register(Post, PostAdmin)

- 自定义字段

    Django Model 提供了比数据库要丰富的字段。如果还不够用，可以自定义字段。


    .. code-block::

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

- Model 继承

    Model 可以继承，继承有三种模式：

        - Abstract: 被继承的 Model, 不会建立对应的表。继承的 Model 会在被继承 Model 的基础上添加字段。

            .. code-block::

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

            .. code-block::

                from django.db import models
                class BaseContent(models.Model):
                    title = models.CharField(max_length=100)
                    created = models.DateTimeField(auto_now_add=True)

                class Text(BaseContent):
                    body = models.TextField()

        - Proxy：被继承的 Model 会建立对应的表，但是继承的 Model 对应的表就是被继承 Model 的表。继承的 Model 是添加了新的方法（不更改字段），方便使用。

            .. code-block::

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


Reference
=========

- Django by Example.
