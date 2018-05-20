=============
Django View
=============

:Author: 王蒙
:Tags: Django, Web Frameworks, Python

:abstract:

    view 负责处理解析 http request ，构造 http response。

.. contents::

Audience
========

Python 开发，网络开发

Prerequisites
=============

Python, 简单了解 http 协议

Problem
=======

如何定义 view


Solution
========

- 定义 view 函数。

    .. code-block::

        from django.http import HttpResponse

        def hello(request):
            # 与 flask 不同， django 的 view 函数必须返回 HttpResponse, 返回字符串是不合法的。
            return HttpResponse("Hello World")


        # view 函数还可以带参数，这个参数一般是取自与 url path 中的参数。
        def get_resource(request, resource_id):
            return HttpResponse("Resource Id is: %s" % resource_id)


    对于带参数的 view 函数，在 route 配置时，需要配置参数取什么值，比如对于上面的 get_resource view 可以在 urls.py 中定义：


    .. code-block::

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


- 定义 view 类，使用类定义 View 最大的好处是可以通过类继承重用代码。`django.views.generic` 有现成的 View 类型，继承这些 View 类型，可以定义 View 类。

    .. code-block::

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





Reference
=========

- Django By Example
