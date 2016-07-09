import tornado.web
import tornado.ioloop
import tornado.template
import datetime
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("base.html", message="hello world!")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
        ],
        template_path=os.path.join(os.getcwd(), "templates"),
        static_path=os.path.join(os.getcwd(), "static"),
    )
    app.listen(50007)
    tornado.ioloop.IOLoop.current().start()
