import settings
import tornado.ioloop
import tornado.web
from page_handlers import *


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
         (r'/login', Login),
         (r'/logout', Logout)],
        debug=True,
        autoreload=True,
        compiled_template_cache=False,
        static_path=settings.STATIC_PATH,
        template_path=settings.TEMPLATE_PATH,
        login_url='/login',
        cookie_secret='j9Wy1m*3CnwKw!AFd5sd3kl@',
        xsrf_cookies=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(8181)
    tornado.ioloop.IOLoop.current().start()
