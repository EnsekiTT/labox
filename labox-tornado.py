import tornado.web
import tornado.ioloop
import tornado.template
import datetime
import os
import settings
import time

class Responder():
    def __init__(self):
        self.first_info = "なんでも話しかけて"
        self.response = []

    def set_name(self, name):
        self.name = name
        self.logined_info = self.name + ", " + self.first_info

    def message_text(self, message):
        message = tornado.escape.xhtml_escape(message)
        self.response.append("えっ？ " + message + "！？")


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect(self.get_argument("next","/face"))
        self.render("main.html")


class FaceHandler(BaseHandler):
    def initialize(self):
        self.res = Responder()

    @tornado.web.authenticated
    def get(self):
        self.res.set_name(tornado.escape.xhtml_escape(self.current_user))
        self.render("face.html", message=self.res.logined_info)

    @tornado.web.authenticated
    def post(self):
        self.res.message_text(self.get_argument("message"))
        self.render("face.html", message=self.res.response[-1])


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        self.set_secure_cookie("user", self.get_argument("user"))
        self.redirect("/")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/?logout=True"))

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/face", FaceHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        ],
        template_path=os.path.join(os.getcwd(), "templates"),
        static_path=os.path.join(os.getcwd(), "static"),
        cookie_secret=settings.cookie_secret,
        login_url='/login',
    )
    app.listen(50007)
    tornado.ioloop.IOLoop.current().start()
