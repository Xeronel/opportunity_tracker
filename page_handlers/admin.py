from .base import BaseHandler
from tornado import gen
from tornado.web import MissingArgumentError, authenticated
from psycopg2 import IntegrityError


class Admin(BaseHandler):
    @gen.coroutine
    @authenticated
    def get(self):
        permissions = yield self.get_permissions()
        user = yield self.get_user()
        self.render('admin.html', permissions=permissions, user=user)

    @gen.coroutine
    @authenticated
    def post(self):
        permissions = yield self.get_permissions()
        user = yield self.get_user()
        if 'adduser' in self.request.arguments:
            self.add_user(permissions)
        self.render('admin.html', permissions=permissions, user=user)

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
                    except MissingArgumentError:
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
            except IntegrityError:
                print('Error: User %s already exists' % self.get_argument('username'))
