import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.gen
from json import loads, dumps
import logging
from time import sleep
import time
from threading import Lock


class MainHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        print("receive request")
        tornado.ioloop.IOLoop.instance().add_callback(self.cost_time_operate)

    def cost_time_operate(self):
        self.write("time cost operate")
        print("time cost operation begins")
        sleep(1)
        print("time cost operation ends")
        print("done")

if __name__ == '__main__':

    tornado.options.define("port", default=8080, help="run on the given port", type=int)

    app = tornado.web.Application(handlers=[(r"/", MainHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(4000)
    tornado.ioloop.IOLoop.instance().start()
