import config
import tornado.ioloop
import tornado.web
import tornado.gen
from database import Database
from page_handlers import *
from page_handlers import api
import ui_modules


def make_app():
    return tornado.web.Application(
        [(r'/api/v1/company/(.*)/(.*)', api.Company),
         (r'/api/v1/company/(.*)', api.Company),
         (r'/api/v1/contact/(.*)/(.*)', api.Contact),
         (r'/api/v1/contact/(.*)', api.Contact),
         (r'/api/v1/employee/(.*)/(.*)', api.Employee),
         (r'/api/v1/employee/(.*)', api.Employee),
         (r'/api/v1/part/(.*)/(.*)', api.Part),
         (r'/api/v1/part/(.*)', api.Part),
         (r'/api/v1/work_order/(.*)/(.*)', api.WorkOrder),
         (r'/api/v1/work_order/(.*)', api.WorkOrder),
         (r'/api/v1/station/(.*)/(.*)', api.Station),
         (r'/api/v1/station/(.*)', api.Station),
         (r'/', Dashboard),
         (r'/dashboard', Dashboard),
         (r'/calendar', Calendar),
         (r'/(add|rem|mod)_contact', Contact),
         (r'/(add|rem|mod)_company', Company),
         (r'/(add|rem|mod|view)_notification', Notification),
         (r'/(add|rem|mod|view)_notes?', Note),
         (r'/(add|rem|mod)_part', Part),
         (r'/(add|manage)_project', Project),
         (r'/project/(\d+)/([a-zA-Z_\-]+)', ProjectRouter),
         (r'/project/(\d+)/([a-zA-Z_\-]+)/(.*)', ProjectRouter),
         (r'/(work_order)', WorkOrder),
         (r'/get_notes/(.*)', GetNotes),
         (r'/get_contacts/(.*)', GetContacts),
         (r'/print', Print),
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
    app.listen(config.web.port)

    # Attempt to connect to the database
    ioloop = tornado.ioloop.IOLoop.current()
    app.database = Database(ioloop)
    future = app.database.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    # Start the app
    ioloop.start()
