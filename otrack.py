from config import Config
import tornado.ioloop
import tornado.web
from tornado import gen
import momoko
import psycopg2
from page_handlers import *
import ui_modules
import ui_methods


class Admin(BaseHandler):
    @gen.coroutine
    def get(self):
        permissions = yield self.get_permissions()
        self.render('admin.html', permissions=permissions)

    @gen.coroutine
    def post(self):
        permissions = yield self.get_permissions()
        if 'adduser' in self.request.arguments:
            self.add_user(permissions)
        self.render('admin.html', permissions=permissions)

    def add_user(self, permissions):
        if 'add_user' in permissions and permissions['add_user']:
            try:
                # Try to add the user to the database and return the new user ID
                cursor = yield self.db.execute(
                    "INSERT INTO employee (pwhash, username, first_name, last_name, email) VALUES "
                    "(crypt(%(passwd)s, gen_salt('bf')), %(username)s, %(first_name)s, %(last_name)s, %(email)s) "
                    "RETURNING id;",
                    {'passwd': self.get_argument('password'),
                     'username': self.get_argument('username'),
                     'first_name': self.get_argument('firstname'),
                     'last_name': self.get_argument('lastname'),
                     'email': self.get_argument('email')})
                uid = cursor.fetchone()[0]

                # Store new users permissions
                user_perms = {'employee': uid}
                for perm in ['add_user', 'delete_user', 'change_other_password']:
                    try:
                        arg = self.get_argument(perm)
                        if arg == 'on':
                            user_perms[perm] = True
                        else:
                            user_perms[perm] = arg
                    except tornado.web.MissingArgumentError:
                        pass

                # Permission's to be set
                columns = [k for k in user_perms]

                # If any of the admin columns are set then the user is an admin
                if len({'add_user', 'delete_user', 'change_password'}.intersection(set(columns))) > 0:
                    columns.append('admin')
                    user_perms['admin'] = True

                # Calculate the number of permissions that will be inserted
                values = '%s, ' * len(columns)
                values = values[:-2]

                # Get the permission values to be set
                params = tuple([user_perms[k] for k in columns])

                # Set the new users permissions
                cursor = yield self.db.execute(
                    "INSERT INTO permissions "
                    "(%s) " % ', '.join(columns) +
                    "VALUES (%s)" % values, params)
            except psycopg2.IntegrityError:
                print('Error: User %s already exists' % self.get_argument('username'))


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
