import tornado.web
import tornado.ioloop
import tornado.template
import datetime
import os
import settings
import sqlite3
import json


class Responder():
    def __init__(self):
        self.first_info = "なんでも話しかけて"
        self.response = []

    def set_name(self, name):
        self.name = name
        self.signined_info = self.name + ", " + self.first_info

    def message_text(self, message):
        message = tornado.escape.xhtml_escape(message)
        self.response.append("えっ？ " + message + "！？")

class DatabaseExample():
    def __init__(self):
        self.dbPath = 'database.db'

    def connect(self):
        self.connection = sqlite3.connect(self.dbPath)
        self.cursorobj = connection.cursor()

    def disconnect(self):
        self.connection.close()

    def _query(self, query):
        try:
            self.cursorobj.execute(query)
            result = self.cursorobj.fetchall()
            self.connection.commit()
            return result
        except Exception:
            raise



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
        self.render("face.html", message=self.res.signined_info)

    @tornado.web.authenticated
    def post(self):
        self.res.message_text(self.get_argument("message"))
        self.render("face.html", message=self.res.response[-1])

class SigninHandler(BaseHandler):
    def get(self):
        self.render("signin.html")

    def post(self):
        self.set_secure_cookie("user", self.get_argument("user"))
        self.redirect("/")


class SignoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/?signout=True"))

class SignupHandler(BaseHandler):
    def get(self):
        self.render("signup.html")

    def post(self):
        username = self.get_argument("")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/face", FaceHandler),
        (r"/signin", SigninHandler),
        (r"/signout", SignoutHandler),
        (r"/signup", SignupHandler),
        ],
        template_path=os.path.join(os.getcwd(), "templates"),
        static_path=os.path.join(os.getcwd(), "static"),
        cookie_secret=settings.cookie_secret,
        login_url='/signin',
    )
    app.listen(50007)
    tornado.ioloop.IOLoop.current().start()
