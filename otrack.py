from config import Config
import tornado.ioloop
import tornado.web
import momoko
from page_handlers import *
import ui_modules
import ui_methods


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
        debug=config.debug,
        autoreload=config.autoreload,
        compiled_template_cache=config.compiled_template_cache,
        static_path=config.static_path,
        template_path=config.template_path,
        login_url='/login',
        cookie_secret=config.cookie_secret,
        key_version=config.key_version,
        xsrf_cookies=True,
        ui_modules=ui_modules,
        ui_methods=ui_methods)


if __name__ == '__main__':
    # Initialize config
    config = Config()

    # Create a new web application
    app = make_app()
    app.listen(8181)

    # Attempt to connect to the database
    ioloop = tornado.ioloop.IOLoop.current()
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
