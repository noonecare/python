============
Restful API
============

:Author: 王蒙
:Tags: Django, Web Frameworks, Rest ful, API

:abstract:

    不用任何插件，django 就可以实现 restful API。但是在 rest-framework 的帮助下，更容易写出标准，规范的 Restful API。

.. contents::

Audience
========

Python 开发，网站开发

Prerequisites
=============

python, Restful API


Problem
=======

- Restful 常见误区以及 rest-framework 的优势
- Serializer
- Parsers/Renderers
- Generic APIView
- authentication and permission
- viewset and router

Solution
========

- Restful 常见误区以及 rest-framework 的优势

    - http 服务，返回 json 就是 restful 接口；返回 html 网页就不是 restful 接口。

        Restful 是为方便前后端沟通而设计的规范。具体特征是： Resource-Oriented, Stateless。
        http 协议是网络协议，http 服务可能遵守 Restful API 的规范，也可能不遵守 Restful API 的规范。
        http 协议很容易符合 Restful 规范。使用 http 协议注意实现如下几点就能够实现 Restful 规范。

            - Resource-Oriented，尽量用名词设计 API。对于资源的操作，使用 http 方法来完成。
            - 使用 Content-Type 控制资源的表现形式。json，xml 是常用的表现形式，标准的 Restful API 一般会提供多种表现形式，用 Content-Type 确定到底如何展现。
            - GET, HEAD 不修改资源。POST 修改资源。
            - 返回码，返回信息要自说明（self-document）。力求做到用只要看返回，就知道请求的操作怎么样了。
            - 状态转移通过 url 连接跳转。

    - rest-framework 的优势

        刚刚的论述，已经说明不是简单写个返回值是 json 字符串的 view，就能整出标准的 restful 接口（之前这样写的 restful API 是不太规范的）。

        rest-frameworks 为写 Restful API 提供了 GenericView, Parser and Render, Permission Control 。使用这些现成的组件，方便写出规范的 Restful API。

- Serializer

    Restful API 要做的事儿，可能是去查询数据库。对于数据库定义 Serializer/Deserializer 可以方便的把数据库查询结果整成 Restful 接口的返回值。

    rest-framework 提供了三个 serializer 基类：

        - Serializer: Provides serialization for normal Python class instances
        - ModelSerializer: Provides serialization for model instances
        - HyperlinkedModelSerializer: The same as ModelSerializer, but represents object relationships with links rather than primary keys

    .. code-block:: python

        from rest_framework import serializers
        from ..models import Subject
        class SubjectSerializer(serializers.ModelSerializer):
            class Meta:
                model = Subject
                fields = ('id', 'title', 'slug')


    对于有外键的 model ， serializer 既可以选择呈现外键的值（integer），也可以选择呈现外键对应的对象。

        .. code-block:: python

            class CourseSerializer(serializers.ModelSerializer):
                # 选择呈现外键的值（integer）
                modules = ModuleSerializer()

                class Meta:
                    model = Course
                    fields = ('id', 'subject', 'title', 'slug',
                              'overview', 'created', 'owner', 'modules')



        .. code-block:: python

            class CourseSerializer(serializers.ModelSerializer):
                # 选择呈现外键对应的对象
                modules = ModuleSerializer(many=True)

                class Meta:
                    model = Course
                    fields = ('id', 'subject', 'title', 'slug',
                              'overview', 'created', 'owner', 'modules')

- parsers and renderers

    在 django project 的 settings.py 文件配置 parsers and renders，restful api 就会根据设计根据 Content-Type header 来表现返回结果。上面的 serializer 是把数据转成字典，而 parsers/renders 是把返回结果整成二进制串。

    可能会配置 settings.py 中的 REST_FRAMEWORK -> DEFAULT_RENDERER_CLASSES 项。这样这个 project 默认会用这些 renders。

    parsers 和 renderers 更多细节，参见：

        - http://www.django-rest-framework.org/api-guide/renderers/
        - http://www.django-rest-framework.org/api-guide/parsers/


- Generic API View

    .. code-block:: python

        from rest_framework import generics
        from ..models import Subject
        from .serializers import SubjectSerializer

        # 如果Restful API 的返回结果是从 QuerySet 中取出来的。那么继承 ListAPIView 和 RetrieveAPIView 可以方便地构造Restful API。
        class SubjectListView(generics.ListAPIView):
            queryset = Subject.objects.all()
            serializer_class = SubjectSerializer

        class SubjectDetailView(generics.RetrieveAPIView):
            queryset = Subject.objects.all()
            serializer_class = SubjectSerializer


        # 如果Restful API 的返回结果不是从 QuerySet 中取出来的。可以继承 APIView 自定义返回值。
        from django.shortcuts import get_object_or_404
        from rest_framework.views import APIView
        from rest_framework.response import Response
        from ..models import Course
        class CourseEnrollView(APIView):
            def post(self, request, pk, format=None):
                course = get_object_or_404(Course, pk=pk)
                course.students.add(request.user)
                return Response({'enrolled': True})


- authentication and permissions

        rest-framework 提供了 `BasicAuthentication`, `TokenAuthentication` 和 `SessionAuthentication` 类实现认证。

        rest-frameworks 提供了 `AllowAny`, `IsAuthenticated`, `IsAuthenticatedOrReadOnly`, `DjangoModelPermissions` 和 `DjangoObjectPermissions` 类实现权限控制。

        .. code-block:: python

            from rest_framework.authentication import BasicAuthentication
            from rest_framework.permissions import IsAuthenticated
            class CourseEnrollView(APIView):
                # 指明采用哪个类，做认证
                authentication_classes = (BasicAuthentication,)
                # 指明是什么什么样的权限控制，比如这里 IsAuthenticated 表示只有认证用户才能使用这个 view（API）
                permission_classes = (IsAuthenticated,)
                # ...

        继承 `rest_framework.permission.BasePermission`，重写下面两种方法，可以自定义 permission。

            - has_permission(): View-Level permission check。
            - has_object_permission(): Object-Level permission check。

        .. code-block:: python

            from rest_framework.permissions import BasePermission
            class IsEnrolled(BasePermission):

            def has_object_permission(self, request, view, obj):
                return obj.students.filter(id=request.user.id).exists()

- viewset and router

    Viewset 可以使用 router 绑定 url。在 Viewset 中 view 比较多时，会很有用。

    .. code-block:: python

        from django.conf.urls import url, include
        from rest_framework import routers
        from . import views


        router = routers.DefaultRouter()
        router.register('courses', views.CourseViewSet)

    .. code-block:: python

        class CourseViewSet(viewsets.ReadOnlyModelViewSet):
            queryset = Course.objects.all()
            serializer_class = CourseSerializer

            @detail_route(methods=['post'],
                          authentication_classes=[BasicAuthentication],
                          permission_classes=[IsAuthenticated])
            def enroll(self, request, *args, **kwargs):
                course = self.get_object()
                course.students.add(request.user)
                return Response({'enrolled': True})

            @detail_route(methods=['get'],
                          serializer_class=CourseWithContentsSerializer,
                          authentication_classes=[BasicAuthentication],
                          permission_classes=[IsAuthenticated, IsEnrolled])
            def contents(self, request, *args, **kwargs):
                return self.retrieve(request, *args, **kwargs)


Reference
=========

- Django By Example
- rest-framework 文档： http://www.django-rest-framework.org/
