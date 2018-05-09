===========
WSGI
===========

:Author: 王蒙
:Tags: 网络编程

:abstract:

    **wsgi** 协议是 Application 和 Server 通信的标准接口。要实现 wsgi 的 Application 和 Server 必须遵守 wsgi 协议。遵守这个协议，就可以混合使用各种 wsgi Application 和 wsgi Server。这和让各种牌子的电脑和U盘支持统一的 USB 口，那么任何电脑都可以和任意 U 盘连接是一个道理。

.. contents::

Audience
========

网络编程

Prerequisites
=============




Problem
=======

- wsgi 的优势
- wsgi 协议
- 写 wsgi 的方式
- wsgi 的常见应用
- wsgi 与 server 的兼容


Solution
========

wsgi 的优势
^^^^^^^^^^^^^^

    兼容性是 wsgi 的突出优势。 wsgi 接收请求，构造响应，实现了 Application 的处理逻辑。和采用指定 Web Frameworks 方式写 Application 不同，采用 wsgi 协议写的 Application ，可以兼容很多 Server。

wsgi 协议
^^^^^^^^^^^^^^^

`PEP 3333`_ 详细介绍了 wsgi 协议。

wsgi 协议对于 wsgi Application 的要求：
    -  Application 是个 callable 的 object， 函数和类都可以。
    - Application callable 接收两个参数 `envrion` 和 `start_response`。
        - `environ`: environ 包含了 http 请求的所有字段。详细 `envrion` 中必须包含哪些字段，请查考 `PEP 3333`_ 。
        - `start_response`: start_response 表示开始返回 response, `start_response(status, headers)` 接收 status(比如 '200 OK') 和 headers(比如 ['Content-Type': 100])， wsgi 在调用 `start_response(status, headers)` 之后会用 `return` 或者 `yield` 把 response 的 body 传递出去。常见 headers 的含义，请参考 http 协议的标准。
    - Application 的返回值是由 bytes 组成的 iterable 的 object。

wsgi 协议对于 Server 的要求：

    - 可以把 Server 想象成之前用 socket 写的服务器，主要负责侦听用户的连接请求。
    - 当有 client 连接到服务器之后，Server 就把请求转成 `envrion` （附带些 Server 本身提供的信息）传递给 wsgi Application 去处理， wsgi Application 返回的 response 传递给 Server, Server 把这个 response 传递给 client。



写 wsgi 协议的方式
^^^^^^^^^^^^^^^^^^^^^^

不使用第三方包的方式， 主要分两步：

    - 从 `environ` 中解析出 http request 中的字段。
    - 根据 http request 的字段，构造 http response。


使用 `webob` 包：

    - `webob` 提供了 `webob.Request` 和 `webob.Response` 方便解析 request 和构造 response。
    - `timeapp_webob.py`_ 是使用 `webob` 定义 wsgi 的例子。

使用 `werkzeug` 包：

    - 直观的 http 处理逻辑是，收到 http request, 返回 http response。`werkzeug` 允许我们定义一个接收 request 参数，返回 response 的函数。我们定义的这个函数经 `werkzeug.wrappers.Request.application` 装饰器装饰，就变成 wsgi。
    - `werkzeug` 提供的 request 和 response, 要比 wsgi 原生提供的 environ 和 start_response， 方便解析请求和构造响应。
    - `timeapp_werkz.py`_ 是使用 `werkzeug` 定义 wsgi 的例子。

wsgi 写 middleware
^^^^^^^^^^^^^^^^^^^^^^^^^^^

request/reponse 在 Server 和 Application 之间传递时，可以通过一个组件处理。这个组件就是中间件。比如 Dispatch 请求的逻辑可以写到中间件了。

.. code-block::

    # This dispatcher is just for demonstration.

    from wsgiref.simple_server import make_server

    URL_PATTERNS = (
        ('/hi', 'say_hi'),
        ('/hello', 'say_hello'),
    )


    class Dispatcher(object):
        def _match(self, path):
            path = path.split('/')[1]
            for url, app in URL_PATTERNS:
                if path in url:
                    return app

        def __call__(self, environ, start_response):
            path = environ.get('PATH_INFO')
            app = self._match(path)
            if app:
                app = globals()[app]
                return app(environ, start_response)
            else:
                start_response("404 NOT FOUND", [('Content-Type', 'text/plain')])
                return [b"Page does not exists"]


    def say_hi(environ, start_response):
        start_response("200 OK", [('Content-Type', 'text/plain')])
        return [b'wangmeng say hi to you!']


    def say_hello(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'wangmeng say hi to you!']


    app = Dispatcher()

    httpd = make_server('', 8000, app)
    httpd.serve_forever()



wsgi Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^

早期 python 性能不行，python 定义的 wsgi application 会装到 Apache Server 上。

后来，出现了一堆 python Server(gunicorn, flask, django 等等)， python wsgi 也可以安装到这些 python server 上。`gunicorn`_ 运行 wsgi 最为方便。

wsgi 不能兼容到采用异步方式实现的 Server 中，比如 wsgi 和 tornado 不兼容（可以强行让 tornado 使用 wsgi 但是性能会打折扣）。实际上采用异步实现的 Server 兼容性很差，采用了某个异步 Server, 一般也就不得不采用 Server 指定的 Frameworks 去写 Application。


Reference
=========

- Foundations of Python Networks Programming
- PEP 3333: https://www.python.org/dev/peps/pep-3333/

.. _PEP 3333: https://www.python.org/dev/peps/pep-3333/
.. _timeapp_werkz.py: https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter10/timeapp_werkz.py
.. _timeapp_webob.py: https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter10/timeapp_webob.py
.. _gunicorn: http://gunicorn.org/