import settings
import tornado.ioloop
import tornado.web
import tornado.escape


class MainHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user')

    def get(self):
        self.render('dashboard.html')

    def post(self):
        self.set_secure_cookie('user', self.get_argument('name'))
        self.redirect('/')


class Dashboard(tornado.web.RequestHandler):
    def get(self):
        self.render('dashboard.html')


class Calendar(tornado.web.RequestHandler):
    def get(self):
        self.render('calendar.html')


class Company(tornado.web.RequestHandler):
    def get(self):
        self.render('company.html')

    def post(self):
        print(self.get_argument('companyname'))
        print(self.get_argument('industry'))
        self.render('company.html')


class Contact(tornado.web.RequestHandler):
    def get(self):
        self.render('contact.html')


class Notification(tornado.web.RequestHandler):
    def get(self):
        self.render('notification.html')


class Note(tornado.web.RequestHandler):
    def get(self):
        self.render('note.html')


def make_app():
    return tornado.web.Application(
        [(r'/', Dashboard),
         (r'/dashboard', Dashboard),
         (r'/calendar', Calendar),
         (r'/add_company', Company),
         (r'/add_contact', Contact),
         (r'/add_notification', Notification),
         (r'/add_note', Note)],
        debug=True,
        autoreload=True,
        compiled_template_cache=False,
        static_path=settings.STATIC_PATH,
        template_path=settings.TEMPLATE_PATH,
        cookie_secret='j9Wy1m*3CnwKw!AFd5sd3kl@')


if __name__ == '__main__':
    app = make_app()
    app.listen(8181)
    tornado.ioloop.IOLoop.current().start()
