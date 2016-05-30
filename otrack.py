import settings
import tornado.ioloop
import tornado.web
import tornado.escape
from tornado.escape import json_encode

companies = set()
contacts = {}
notes = {}


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')


class Login(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect('/dashboard')
        else:
            self.render('login.html')

    def post(self):
        try:
            next_page = self.get_argument('next')
        except tornado.web.MissingArgumentError:
            next_page = '/dashboard'

        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect(next_page)


class Logout(BaseHandler):
    def get(self):
        self.clear_cookie('username')
        self.redirect('/login')


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.redirect('/dashboard')


class Dashboard(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        username = self.current_user
        self.render('dashboard.html', username=username)


class Calendar(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('calendar.html')


class Industry(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('industry.html')

    @tornado.web.authenticated
    def post(self):
        self.render('industry.html')
        print(self.get_argument('industry'))


class Company(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('company.html')

    @tornado.web.authenticated
    def post(self):
        company = self.get_argument('company')
        if company:
            companies.add(company)
        self.render('company.html')


class Contact(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('contact.html', companies=companies)

    @tornado.web.authenticated
    def post(self):
        company = self.get_argument('company')
        first_name = self.get_argument('firstname')
        last_name = self.get_argument('lastname')
        title = self.get_argument('title')
        email = self.get_argument('email')
        phone = self.get_argument('phone')

        if company not in contacts:
            contacts[company] = []
        contacts[company].append({'first_name': first_name,
                                  'last_name': last_name,
                                  'title': title,
                                  'email': email,
                                  'phone': phone})
        self.render('contact.html', companies=companies)


class Notification(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('notification.html', companies=companies)

    @tornado.web.authenticated
    def post(self):
        self.render('notification.html', companies=companies)


class Note(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('note.html',
                    companies=companies,
                    contacts=contacts,
                    notes=notes)

    @tornado.web.authenticated
    def post(self):
        company = self.get_argument('company')
        action = self.get_argument('action')
        note = self.get_argument('note')
        date = self.get_argument('date')
        try:
            contact = int(self.get_argument('contact'))
        except ValueError:
            raise tornado.web.HTTPError(400, 'contact must be an integer')

        # Store note
        if company not in notes:
            notes[company] = []
        notes[company].append({'action': action,
                               'note': note,
                               'date': date,
                               'contact': contact})
        self.render('note.html',
                    companies=companies,
                    notes=notes)


class GetNotes(BaseHandler):
    @tornado.web.authenticated
    def get(self, company):
        if company in notes:
            self.render('get_notes.html',
                        notes=notes[company][-5:],
                        contacts=contacts[company], )
        else:
            self.write('')


class GetContacts(BaseHandler):
    @tornado.web.authenticated
    def get(self, company):
        if company in contacts:
            self.write(json_encode(
                [{'text': '%s %s' % (contact['first_name'], contact['last_name']),
                  'value': idx}
                 for idx, contact in enumerate(contacts[company])]))
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
