import tornado.web
from tornado import gen


class User:
    def __init__(self, uid, first_name, last_name, email):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        if self.get_secure_cookie('username') is None or self.get_secure_cookie('uid') is None:
            return None
        else:
            return self.get_secure_cookie('username')

    @gen.coroutine
    def get_user(self):
        uid = self.get_secure_cookie('uid').decode('utf-8')
        cursor = yield self.db.execute("SELECT id, first_name, last_name, email FROM employee "
                                       "WHERE (id = %(uid)s)", {'uid': uid})
        uid, first_name, last_name, email = cursor.fetchone()
        return User(uid, first_name, last_name, email)

    def get_first_name(self):
        return self.get_cookie('first_name')

    def get_last_name(self):
        return self.get_cookie('last_name')

    @gen.coroutine
    def get_permissions(self):
        cursor = yield self.db.execute(
            "SELECT add_user, delete_user, change_other_password, admin FROM permissions "
            "INNER JOIN employee ON (permissions.employee = employee.id) "
            "WHERE (employee.username = %(username)s);",
            {'username': self.current_user.decode('utf-8')})
        add_user, delete_user, change_other_password, admin = cursor.fetchone()
        return {'add_user': add_user,
                'delete_user': delete_user,
                'change_other_password': change_other_password,
                'admin': admin}

    @gen.coroutine
    def get_employees(self):
        cursor = yield self.db.execute("SELECT id, first_name, last_name FROM employee "
                                       "ORDER BY first_name ASC, last_name ASC;")
        return cursor.fetchall()

    @property
    def db(self):
        return self.application.db
