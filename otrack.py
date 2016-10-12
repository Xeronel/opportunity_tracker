import config
import tornado.ioloop
import tornado.web
import tornado.gen
import psycopg2
import momoko
from page_handlers import *
from page_handlers import api
import ui_modules


class Database:
    def __init__(self):
        self.pool = momoko.Pool(dsn="dbname=%s user=%s password=%s host=%s port=%s" %
                                    (config.db.database, config.db.username, config.db.password,
                                     config.db.hostname, config.db.port),
                                size=1,
                                max_size=config.db.max_size,
                                auto_shrink=config.db.auto_shrink,
                                ioloop=ioloop)

    def connect(self):
        return self.pool.connect()

    @tornado.gen.coroutine
    def execute(self, *args, **kwargs):
        # Throws momoko.PartiallyConnectedError if database is down
        try:
            cursor = yield self.pool.execute(*args, **kwargs)
        except psycopg2.OperationalError:
            yield self.connect()
            cursor = yield self.pool.execute(*args, **kwargs)
        return cursor


def make_app():
    return tornado.web.Application(
        [(r'/api/v1/company/(.*)/(.*)', api.Company),
         (r'/api/v1/company/(.*)', api.Company),
         (r'/api/v1/contact/(.*)/(.*)', api.Contact),
         (r'/api/v1/contact/(.*)', api.Contact),
         (r'/api/v1/employee/(.*)/(.*)', api.Employee),
         (r'/api/v1/employee/(.*)', api.Employee),
         (r'/', Dashboard),
         (r'/dashboard', Dashboard),
         (r'/calendar', Calendar),
         (r'/add_industry', Industry),
         (r'/(add|rem|mod)_contact', Contact),
         (r'/(add|rem|mod)_company', Company),
         (r'/(add|rem|mod|view)_notification', Notification),
         (r'/(add|rem|mod|view)_notes?', Note),
         (r'/(add|rem|mod)_part', Part),
         (r'/(add|manage)_project', Project),
         (r'/project/(\d+)/([a-zA-Z_\-]+)', ProjectRouter),
         (r'/project/(\d+)/([a-zA-Z_\-]+)/(.*)', ProjectRouter),
         (r'/get_notes/(.*)', GetNotes),
         (r'/get_contacts/(.*)', GetContacts),
         (r'/admin', Admin),
         (r'/clear_company', ClearCompany),
         (r'/profile', Profile),
         (r'/login', Login),
         (r'/logout', Logout)],
        debug=config.web.debug,
        autoreload=config.web.autoreload,
        compiled_template_cache=config.web.compiled_template_cache,
        static_path=config.web.static_path,
        template_path=config.web.template_path,
        login_url='/login',
        cookie_secret=config.web.cookie_secret,
        key_version=config.web.key_version,
        xsrf_cookies=True,
        ui_modules=ui_modules)


if __name__ == '__main__':
    # Create a new web application
    app = make_app()
    app.listen(8181)

    # Attempt to connect to the database
    ioloop = tornado.ioloop.IOLoop.current()
    app.database = Database()
    future = app.database.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    # Start the app
    ioloop.start()
