import settings
import tornado.ioloop
import tornado.web
import tornado.escape


companies = set()
notes = {}


class MainHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user')

    def get(self):
        self.render('dashboard.html')

    def post(self):
        self.set_secure_cookie('user', self.get_argument('name'))
        self.redirect('/')


class Dashboard(tornado.web.RequestHandler):
    def get(self):
        self.render('dashboard.html')


class Calendar(tornado.web.RequestHandler):
    def get(self):
        self.render('calendar.html')


class Industry(tornado.web.RequestHandler):
    def get(self):
        self.render('industry.html')

    def post(self):
        self.render('industry.html')
        print(self.get_argument('industry'))


class Company(tornado.web.RequestHandler):
    def get(self):
        self.render('company.html')

    def post(self):
        company = self.get_argument('company')
        if company:
            companies.add(company)
        self.render('company.html')


class Contact(tornado.web.RequestHandler):
    def get(self):
        self.render('contact.html', companies=companies)

    def post(self):
        self.render('contact.html', companies=companies)


class Notification(tornado.web.RequestHandler):
    def get(self):
        self.render('notification.html', companies=companies)

    def post(self):
        self.render('notification.html', companies=companies)


class Note(tornado.web.RequestHandler):
    def get(self):
        self.render('note.html',
                    companies=companies,
                    notes=notes)

    def post(self):
        company = self.get_argument('company')
        action = self.get_argument('action')
        note = self.get_argument('note')
        date = self.get_argument('date')

        # Store note
        if company not in notes:
            notes[company] = []
        notes[company].append({'action': action,
                               'note': note,
                               'date': date})
        self.render('note.html',
                    companies=companies,
                    notes=notes)


class GetNotes(tornado.web.RequestHandler):
    def get(self, company):
        if company in notes:
            self.render('get_notes.html', notes=notes[company][-5:])
        else:
            self.write('')


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
         (r'/get_notes/(.*)', GetNotes)],
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
