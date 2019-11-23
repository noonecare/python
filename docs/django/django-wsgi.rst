============
DJANGO WSGI
============

:作者: 王蒙
:标签: Django, WSGI

:简介:

    分析 Django 实现 WSGI 协议的源码。

.. contents::

目标读者
========

Django 开发相关

预备知识
=============

python, WSGI 协议


问题
=======

- Django 是如何实现 WSGI 协议的
- WSGI Server, WSGI Application 是如何协作为用户提供服务的
- Django 中 request -> response 的整个流程是怎样的


解决办法
========


Django 是如何实现 WSGI 协议的
----------------------------------------



Django 中的 WSGIHandler 定义了 WSGI Application , 具体代码如下。其中 WSGIHandler 继承自 BaseHandler 的 get_response 方法，get_response 方法描述了 Django 处理 request-> response 的整个流程，稍后会介绍。


.. code:: python


    class WSGIHandler(base.BaseHandler):
        request_class = WSGIRequest
    
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.load_middleware()
    
        def __call__(self, environ, start_response):
            set_script_prefix(get_script_name(environ))
            signals.request_started.send(sender=self.__class__, environ=environ)
            request = self.request_class(environ)
            response = self.get_response(request)
    
            response._handler_class = self.__class__
    
            status = '%d %s' % (response.status_code, response.reason_phrase)
            response_headers = [
                *response.items(),
                *(('Set-Cookie', c.output(header='')) for c in response.cookies.values()),
            ]
            start_response(status, response_headers)
            if getattr(response, 'file_to_stream', None) is not None and environ.get('wsgi.file_wrapper'):
                response = environ['wsgi.file_wrapper'](response.file_to_stream, response.block_size)
            return response



WSGIServer 和 WSGI Application 是如何配合为用户提供服务的
-------------------------------------------------------------


有三个概念 Server, Handler, WSGI Application , 这几个概念的关系如下：

    1. Server 对象的 wsgi_app 属性记录我们使用那个 wsgi application, RequestHandlerClass 属性记录我们使用那个 RequestHandler.(参考 python wsgiref/simple_server.py:ServerHandler 和 socketserver.py:BaseServer)
    2. Server 调用 serve_forever() 方法，提供通信服务。(socketserver.py:BaseServer)
    3. Server.serve_forever() 方法调用 self.RequestHandlerClass() 处理每个请求。(socketserver.py:BaseServer)
    4. RequestHandlerClass 的 __init__ 方法，会调用 self.handle() 方法处理请求, 会保存 server 属性记录关联的 server。 会定义 start_response 方法。(socketserver.py:BaseRequestHandler, wsgiref/handlers.py:BaseHandler)
    5. RequestHandlerClass 的 handle() 方法，会根据 socket 收到的字节流，解析出 envrion, 然后调用 self.server.wsgi_app(envrion, self.start_response).(wsgiref/handlers.py:BaseHandler).

.. code:: python

    class Server:
        def __init__(self, RequestHandlerClass, wsgi_app, ...):
          ...
          self.RequestHandlerClass = RequestHandlerClass
          self.wsgi_app = wsgi_app
    
        def serve_forever(self):
            for loop:
                # handle a request,
                Handler(request)
   
    class Handler:
        def __init__(self, request, client_address, server):
            self.request = request
            self.client_address = client_address
            self.server = server
            self.setup()
            try:
                self.handle()
            finally:
                self.finish()

       def handle():
           envrion = self.get_envrion()
           self.result = self.server.wsgi_app(environ, self.start_response)
           


Django 中 request -> response 的整个流程是怎样的
--------------------------------------------------------------------------------


Django 为写 WSGI Application 提供了 HttpRequest, HttpResponse, MiddlewareMixin, View 等抽象。
其中 django/django/core/handlers.py 中的 django/core/handlers/base.py:BaseHandler 中的 get_response 方法，描述了 request -> response 的整个流程。值得分析。 


Middleware 可能定义：

    1. process_request(self, request) -> response or None.
    2. process_response(self, request, response) ->  response.
    3. process_view(self, request, callback, callback_args, callback_kwargs) ->  response or None.
    4. process_template_response(self, request, response) -> response or None.
    5. process_exception(self, request, exception) -> response or None.



阅读 django/django/core/handlers/base.py:BaseHandler 中的 _load_middleware()  和 _get_response() 方法，可知：

    1. 在配置文件中配置了 settings.MIDDLEWARE 配置。
    2. 按照 settings.MIDDLEWARE 中的顺序，依次执行 middleware 的 process_request 方法，如果process_request 返回 None， 执行下一个 middleware 的 process_request 方法，如果返回 response 直接跳到处理 response  的流程。
    3. 执行完所有 middleware 中的 process_request 方法后，开始依次执行 middleware 中的 process_view 方法。如果方法返回 None，执行下一个 middleware , 如果返回 response 直接跳到处理 response 的流程。
    4. 执行 view 。
    5. 如果 response 需要 render, 按照 settings.MIDDLEWARE 的逆序，依次执行 process_template_response 方法。如果方法返回 None， 执行下一个 middleware, 如果返回 response 。
    6. 按照 settings.MIDDLEWARE 的逆序，依次执行middleware 中的 process_response 方法。
    7. 处理流程如果发生异常， 按照 settings.MIDDLEWARE 的逆序，依次处理异常。



在 BaseHandler._get_response  方法中，我们可以看到 Django 提供了 resolver 完成从 request.path_info 中解析出 （callable, callable_args, callable_kwargs）的功能。具体 resolver 是如何完成解析的，在 django-resolver 中介绍。


.. code:: python

    class MiddlewareMixin:
        def __init__(self, get_response=None):
            self.get_response = get_response
            super().__init__()
    
        def __call__(self, request):
            response = None
            if hasattr(self, 'process_request'):
                response = self.process_request(request)
            response = response or self.get_response(request)
            if hasattr(self, 'process_response'):
                response = self.process_response(request, response)
            return response



参考文献
=========

- rest-framework 文档： http://www.django-rest-framework.org/
- django 源码: https://github.com/django/django
