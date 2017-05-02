import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.gen
from time import sleep


class MainHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        print("receive request")
        yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_callback)
        # 下面是耗时的操作，这里用 sleep 做例子
        self.write("time cost operate")
        print("time cost operation begins")
        sleep(1)
        print("time cost operation ends")
        print("done")
        self.finish()


if __name__ == '__main__':
    tornado.options.define("port", default=8080, help="run on the given port", type=int)
    app = tornado.web.Application(handlers=[(r"/", MainHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(4000)
    tornado.ioloop.IOLoop.instance().start()
