import settings
import tornado.ioloop
import tornado.web
from tornado import gen
import momoko
import psycopg2
from page_handlers import *
import ui


class Admin(BaseHandler):
    def get(self):
        self.render('admin.html')

    @gen.coroutine
    def post(self):
        if 'adduser' in self.request.arguments:
            try:
                cursor = yield self.db.execute(
                    "INSERT INTO employee (pwhash, username, first_name, last_name, email) VALUES "
                    "(crypt(%(passwd)s, gen_salt('bf')), %(username)s, %(first_name)s, %(last_name)s, %(email)s);",
                    {'passwd': self.get_argument('password'),
                     'username': self.get_argument('username'),
                     'first_name': self.get_argument('firstname'),
                     'last_name': self.get_argument('lastname'),
                     'email': self.get_argument('email')})
            except psycopg2.IntegrityError:
                print('Error: User %s already exists' % self.get_argument('username'))
        self.render('admin.html')


def make_app():
    return tornado.web.Application(
        [(r'/', Dashboard),
         (r'/dashboard', Dashboard),
         (r'/calendar', Calendar),
         (r'/add_industry', Industry),
         (r'/add_company', Company),
         (r'/add_contact', Contact),
         (r'/add_notification', Notification),
         (r'/add_note', Note),
         (r'/get_notes/(.*)', GetNotes),
         (r'/get_contacts/(.*)', GetContacts),
         (r'/admin', Admin),
         (r'/login', Login),
         (r'/logout', Logout)],
        debug=True,
        autoreload=True,
        compiled_template_cache=False,
        static_path=settings.STATIC_PATH,
        template_path=settings.TEMPLATE_PATH,
        login_url='/login',
        cookie_secret='j9Wy1m*3CnwKw!AFd5sd3kl@',
        xsrf_cookies=True,
        ui_modules=ui)


if __name__ == '__main__':
    # Create a new web application
    app = make_app()
    app.listen(8181)

    # Attempt to connect to the database
    ioloop = tornado.ioloop.IOLoop.instance()
    app.db = momoko.Pool(dsn="dbname=sss user=postgres password=DBPASS "
                             "host=localhost port=5432",
                         size=1,
                         ioloop=ioloop)
    future = app.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    # Start the app
    ioloop.start()
