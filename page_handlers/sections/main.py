from page_handlers import BaseHandler
import tornado.web
import tornado.escape
from tornado import gen


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.redirect('/dashboard')


class Dashboard(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        yield self.render('dashboard.html')


class Calendar(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        yield self.render('calendar.html')
