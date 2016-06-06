from .base import BaseHandler
import tornado.web
import tornado.escape
from tornado.escape import json_encode
from tornado import gen
import pycountry

companies = set()
contacts = {}
notes = {}


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.redirect('/dashboard')


class Dashboard(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        user_info = yield self.get_user()
        self.render('dashboard.html', user=user_info)


class Calendar(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        user_info = yield self.get_user()
        self.render('calendar.html', user=user_info)


class Industry(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        user_info = yield self.get_user()
        self.render('industry.html', user=user_info)

    @gen.coroutine
    @tornado.web.authenticated
    def post(self):
        user_info = yield self.get_user()
        self.render('industry.html', user=user_info)
        print(self.get_argument('industry'))


class Company(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        user_info = yield self.get_user()
        employees = yield self.get_employees()
        self.render('company.html',
                    countries=pycountry.countries,
                    user=user_info,
                    employees=employees)

    @gen.coroutine
    @tornado.web.authenticated
    def post(self):
        user_info = yield self.get_user()
        employees = yield self.get_employees()
        company = self.get_argument('company')
        if company:
            companies.add(company)
        self.render('company.html',
                    countries=pycountry.countries,
                    user=user_info,
                    employees=employees)


class Contact(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        user_info = yield self.get_user()
        self.render('contact.html', companies=companies, user=user_info)

    @gen.coroutine
    @tornado.web.authenticated
    def post(self):
        user_info = yield self.get_user()
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
        self.render('contact.html', companies=companies, user=user_info)


class Notification(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        user_info = yield self.get_user()
        self.render('notification.html', companies=companies, user=user_info)

    @gen.coroutine
    @tornado.web.authenticated
    def post(self):
        user_info = yield self.get_user()
        self.render('notification.html', companies=companies, user=user_info)


class Note(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        user_info = yield self.get_user()
        self.render('note.html',
                    companies=companies,
                    contacts=contacts,
                    notes=notes,
                    user=user_info)

    @gen.coroutine
    @tornado.web.authenticated
    def post(self):
        user_info = yield self.get_user()
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
                    notes=notes,
                    user=user_info)


class GetNotes(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self, company):
        user_info = yield self.get_user()
        if company in notes:
            self.render('get_notes.html',
                        notes=notes[company][-5:],
                        contacts=contacts[company],
                        user=user_info)
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
