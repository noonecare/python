import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.gen


class MainHandler(tornado.web.RequestHandler):
    """
    访问这个 http server, 会发现页面一直在加载，永远结束不了。
    这是因为使用 @tornado.web.asynchronous 装饰器之后， 不再默认执行 self.finish(), 你必须在处理了 request 之后，明确指明结
    束 request。
    具体来说，如果 handle request 的方法， 加了 @tornado.web.asynchronous 装饰器，就是必须在处理 request 的代码最后，
    加上 self.finish() 语句
    """

    @tornado.web.asynchronous
    def get(self):
        self.write("Hello World")
        self.set_header("Content-Length", len("Hello World"))

if __name__ == '__main__':
    tornado.options.define("port", default=8080, help="run on the given port", type=int)
    app = tornado.web.Application(handlers=[(r"/", MainHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(4000)
    tornado.ioloop.IOLoop.instance().start()
