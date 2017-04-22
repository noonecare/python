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
        yield self.time_cost_operate()
        print("request, done")
        self.finish()

    @tornado.gen.coroutine
    def time_cost_operate(self):
        """
        tornado.gen.Task 会在当前的Ioloop iteration 中执行 tornado.gen.Task 参数中的函数，yield tornado.gen.Task 后面的语
        句和 tornado.gen.Task 参数中函数，是异步执行的
        add_timeout 会立即执行 epoll 操作
        """
        yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 100)
        sleep(10)
        print("time cost operate")


if __name__ == '__main__':
    tornado.options.define("port", default=8080, help="run on the given port", type=int)
    app = tornado.web.Application(handlers=[(r"/", MainHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(4000)
    tornado.ioloop.IOLoop.instance().start()
