import tornado.web
from tornado import gen


class User:
    def __init__(self, uid, first_name, last_name, email, permissions):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.permissions = permissions


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        username = self.get_secure_cookie('username')
        uid = self.get_secure_cookie('uid')
        if username is None or uid is None:
            return None
        else:
            return username.decode('utf-8') if type(username) == bytes else username

    @gen.coroutine
    @tornado.web.authenticated
    def get_user(self):
        uid = self.get_secure_cookie('uid')
        uid = uid.decode('utf-8') if type(uid) == bytes else uid
        cursor = yield self.db.execute("SELECT id, first_name, last_name, email FROM employee "
                                       "WHERE (id = %(uid)s);", {'uid': uid})
        uid, first_name, last_name, email = cursor.fetchone()
        permissions = yield self.get_permissions()
        return User(uid, first_name, last_name, email, permissions)

    @gen.coroutine
    @tornado.web.authenticated
    def get_permissions(self):
        cursor = yield self.db.execute(
            "SELECT * FROM permissions "
            "INNER JOIN employee ON permissions.employee = employee.id "
            "WHERE employee.username = %(username)s;",
            {'username': self.current_user}
        )
        permissions = cursor.fetchone()
        results = {}
        for i in range(len(cursor.description)):
            results[cursor.description[i].name] = permissions[i]
        return results

    @gen.coroutine
    def get_employees(self):
        cursor = yield self.db.execute("SELECT id, first_name, last_name FROM employee "
                                       "ORDER BY first_name ASC, last_name ASC;")
        return cursor.fetchall()

    @gen.coroutine
    def get_companies(self):
        cursor = yield self.db.execute("SELECT id, name FROM company")
        return cursor.fetchall()

    @property
    def db(self):
        return self.application.db
