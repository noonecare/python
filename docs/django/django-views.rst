=============
Django View
=============

:读者: 王蒙
:标签: Django, Web Frameworks, Python

:简介:

    view 负责处理解析 http request ，构造 http response。

.. contents::

目标读者
========

Python 开发，网络开发

预备知识
=============

Python, 简单了解 http 协议

问题
=======

定义 view

把 view 绑定到指定 url

解决办法
========

定义 view 函数
~~~~~~~~~~~~~~~~~~


使用函数定义 view

.. code-block:: python

    from django.http import HttpResponse

    def hello(request):
        # 与 flask 不同， django 的 view 函数必须返回 HttpResponse, 返回字符串是不合法的。
        return HttpResponse("Hello World")


    # view 函数还可以带参数，这个参数一般是取自与 url path 中的参数。
    def get_resource(request, resource_id):
        return HttpResponse("Resource Id is: %s" % resource_id)

使用类定义 view
~~~~~~~~~~~~~~~~~~~~~~~

使用类最大的好处是可以通过类继承重用代码。`django.views.generic` 有现成的 View 类型，继承这些 View 类型，可以定义 View 类。

.. code-block:: python

    from django.views.generic.base import TemplateResponseMixin, View


    class ContentDeleteView(View):

        def post(self, request, id):
            content = get_object_or_404(Content,
                                        id=id,
                                        module__course__owner=request.user)
            module = content.module
            content.item.delete()
            content.delete()
            return redirect('module_content_list', module.id)


把 view 绑定到指定 url

.. code-block:: python

    from django.conf.urls import url
    from django.contrib import admin

    from .views import get_template, hello, get_resource

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^templates/', get_template),
        url(r'^greet/', hello),
        # 通过如下的方式传递参数
        url(r'(?P<resource_id>\d{4})', get_resource)
    ]


举个例子说明上面urlpatterns 中最后一步 url(r'(?P<resource_id>\d{4})', get_resource) 的用法： 如果输入的 path 为 1234 那么会向 get_resource 传递 {"resource_id": "1234"}。?P 是 Python 正则表达式的用法，re.search("(?P<resource_id>\d{4})", "1234abcd").groupdict() 是使用这种用法的例子。

include(): include url conf

resolve(): 得到 url pattern

reverse()：根据 view 名称和参数值，得出 path

reverse_lazy():

url 和 path 的区别; https://stackoverflow.com/questions/47947673/is-it-better-to-use-path-or-url-in-urls-py-for-django-2-0



参考文献
=========

- Django By Example
- django.urls utility functions: https://docs.djangoproject.com/zh-hans/2.0/ref/urlresolvers/#django.urls.reverse
- django 逆向解析 url: https://www.cnblogs.com/zhenfei/p/6368955.html

