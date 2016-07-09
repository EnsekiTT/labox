import tornado.web
import tornado.ioloop
import tornado.template
import datetime
import os

class Responder():
    def __init__(self):
        self.first_info = "なんでも話しかけて"
        self.response = []

    def message_text(self, message):
        self.response.append("えっ？ " + message + "！？")

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.res = Responder()

    def get(self):
        self.state = "GET"
        self.render("base.html", message=self.res.first_info, state=self.state)

    def post(self):
        self.state = "POST"
        self.res.message_text(self.get_argument("message"))
        self.render("base.html", message=self.res.response[-1], state=self.state)

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
        ],
        template_path=os.path.join(os.getcwd(), "templates"),
        static_path=os.path.join(os.getcwd(), "static"),
    )
    app.listen(50007)
    tornado.ioloop.IOLoop.current().start()
