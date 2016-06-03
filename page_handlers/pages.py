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
    @tornado.web.authenticated
    def get(self):
        self.render('dashboard.html')


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
        self.render('company.html', countries=pycountry.countries)

    @tornado.web.authenticated
    def post(self):
        company = self.get_argument('company')
        if company:
            companies.add(company)
        self.render('company.html', countries=pycountry.countries)


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
