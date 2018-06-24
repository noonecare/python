===============
Django Template
===============

:作者: 王蒙
:标签: Django, Template, Web Framework, Python

:简介:

    介绍 Django 的模板。

.. contents::

目标读者
========

Python 开发，网站开发

预备知识
=============

Python


问题
=======

- 模板继承
- tags
- filters
- context processor
- Pycharm 对于 Django 模板的支持

解决办法
========

- 模板继承

    模板继承，就是通过 {% block {some_name} %}..{% endblock %} 定义 base template。再定义模板时，使用 {% extends "{base template path}"%} 继承 base template。继承模板只能重写 base template 中用 {% block {some_name}%}{% enbblock%} 圈出来的内容， 通过 some_name 连接要替换和被替换的内容。


- tag: 除了模板继承，其他的 tag 都容易理解，基本只要看到 tag 的名字，就能理解。


    - 如果需要某个特别的功能，可以自定义 tag

        - simple_tag

            .. code-block:: python

                from django import template
                register = template.Library()
                from ..models import Post

                @register.simple_tag
                def total_posts():
                    return Post.published.count()

        - inclusion_tag

            .. code-block:: python

                @register.inclusion_tag('blog/post/latest_posts.html')
                def show_latest_posts(count=5):
                    latest_posts = Post.published.order_by('-publish')[:count]
                    return {'latest_posts': latest_posts}



        - assignment_tag

            .. code-block:: python

                from django.db.models import Count
                @register.assignment_tag
                def get_most_commented_posts(count=5):
                    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


- filter: filter 就是在模板中对某些量做处理，比如 uppercase 等。filter 几乎看下名字就知道是什么含义。


    - 对于特别的功能，可以自定义 filter

        .. code-block:: python

            from django.utils.safestring import mark_safe
            import markdown

            @register.filter(name='markdown')
            def markdown_format(text):
                return mark_safe(markdown.markdown(text))

- context processor 从 request 中构造 dict, 这个 dict 可以用在模板中。

    .. code-block:: python

        from .cart import Cart

        def cart(request):
            return {'cart': Cart(request)}

    context processor 要生效，需要写到 settings.py 中。

    .. code-block:: python

        TEMPLATES = [
                        {
                        'BACKEND': 'django.template.backends.django.DjangoTemplates',
                        'DIRS': [],
                        'APP_DIRS': True,
                        'OPTIONS': {
                            'context_processors': [
                            'django.template.context_processors.debug',
                            'django.template.context_processors.request',
                            'django.contrib.auth.context_processors.auth',
                            'django.contrib.messages.context_processors.messages',
                            'cart.context_processors.cart',
                        ],
                        },
                        },
                    ]



- Pycharm

    实际用 Pycharm 写 template 时，会发现 Pycharm 能够自动补全 tag 和 filter。


参考文献
=========

- Django By Example
