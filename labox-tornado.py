import tornado.web
import tornado.ioloop
import tornado.template
import datetime

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader("./static")
        res = loader.load("base.html").generate(message="it works!")
        self.write(res)

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
    ])
    app.listen(50007)
    tornado.ioloop.IOLoop.current().start()
