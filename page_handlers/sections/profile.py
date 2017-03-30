from page_handlers import BaseHandler
from tornado import gen, web


class Profile(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self):
        yield self.render('profile.html')

    @gen.coroutine
    @web.authenticated
    def post(self):
        yield self.change_password()

    @gen.coroutine
    @web.authenticated
    def change_password(self):
        user = yield self.get_user()
        permissions = user.permissions
        password = self.get_argument('password', False)
        if permissions['change_password']:
            if password:
                self.db.execute(
                    "UPDATE employee "
                    "SET pwhash = crypt(%s, gen_salt('bf')) "
                    "WHERE id = %s",
                    [password, user.uid]
                )
            else:
                self.send_error(422)
        else:
            self.send_error(401)
