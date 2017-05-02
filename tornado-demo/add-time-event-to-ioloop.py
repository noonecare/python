import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.gen
from time import sleep
import time


class MainHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        print("receive request")
        yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 10)
        # 下面的代码应该写耗时的操作，这里以 sleep 操作做例子
        sleep(1)
        print("time cost operate")
        self.finish()


if __name__ == '__main__':
    tornado.options.define("port", default=8080, help="run on the given port", type=int)
    app = tornado.web.Application(handlers=[(r"/", MainHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(4000)
    tornado.ioloop.IOLoop.instance().start()
