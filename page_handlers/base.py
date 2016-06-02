import tornado.web
from tornado import gen


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')

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

    @property
    def db(self):
        return self.application.db
