from config import Config
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


def make_app(config):
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
        debug=config.debug,
        autoreload=config.autoreload,
        compiled_template_cache=config.compiled_template_cache,
        static_path=config.static_path,
        template_path=config.template_path,
        login_url='/login',
        cookie_secret=config.cookie_secret,
        key_version=config.key_version,
        xsrf_cookies=True,
        ui_modules=ui)


if __name__ == '__main__':
    # Initialize config
    config = Config()

    # Create a new web application
    app = make_app(config)
    app.listen(8181)

    # Attempt toconnect to the database
    ioloop = tornado.ioloop.IOLoop.instance()
    app.db = momoko.Pool(dsn="dbname=%s user=%s password=%s host=%s port=%s" %
                             (config.database, config.username, config.password,
                              config.hostname, config.port),
                         size=1,
                         max_size=config.max_size,
                         auto_shrink=config.auto_shrink,
                         ioloop=ioloop)
    future = app.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    # Start the app
    ioloop.start()
