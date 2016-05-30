from .interfaces import BaseHandler
from tornado.web import MissingArgumentError


class Login(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect('/dashboard')
        else:
            self.render('login.html')

    def post(self):
        try:
            next_page = self.get_argument('next')
        except MissingArgumentError:
            next_page = '/dashboard'

        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect(next_page)


class Logout(BaseHandler):
    def get(self):
        self.clear_cookie('username')
        self.redirect('/login')
