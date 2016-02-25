import settings
import tornado.ioloop
import tornado.web
import tornado.escape


class MainHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user')

    def get(self):
        self.render('dashboard.html', title='test')

    def post(self):
        self.set_secure_cookie('user', self.get_argument('name'))
        self.redirect('/')


def make_app():
    return tornado.web.Application(
        [(r'/', MainHandler)],
        debug=True,
        autoreload=True,
        compiled_template_cache=False,
        static_path=settings.STATIC_PATH,
        template_path=settings.TEMPLATE_PATH,
        cookie_secret='j9Wy1m*3CnwKw!AFd5sd3kl@')


if __name__ == '__main__':
    app = make_app()
    app.listen(8181)
    tornado.ioloop.IOLoop.current().start()
