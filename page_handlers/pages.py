from .base import BaseHandler
import tornado.web
import tornado.escape
from tornado.escape import json_encode
from tornado import gen
import pycountry

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
        employee = self.get_argument('employee')
        company_name = self.get_argument('company')
        country = self.get_argument('country')
        address1 = self.get_argument('address1')
        try:
            address2 = self.get_argument('address2')
        except tornado.web.MissingArgumentError:
            address2 = ''
        city = self.get_argument('city')
        state = self.get_argument('state')
        postal_code = self.get_argument('zip')
        user_info = yield self.get_user()
        employees = yield self.get_employees()

        cursor = yield self.db.execute("INSERT INTO company (name, active, employee, creator) "
                                       "VALUES (%(company_name)s, %(active)s, %(employee)s, %(creator)s) "
                                       "RETURNING id",
                                       {'company_name': company_name,
                                        'active': True,
                                        'employee': employee,
                                        'creator': user_info.uid})
        company_id = cursor.fetchone()
        cursor = yield self.db.execute(
            "INSERT INTO location (address1, address2, city, state, country, postal_code, company) "
            "VALUES (%(address1)s, %(address2)s, %(city)s, %(state)s, %(country)s, %(postal_code)s, %(company)s)",
            {'address1': address1,
             'address2': address2,
             'city': city,
             'state': state,
             'country': country,
             'postal_code': postal_code,
             'company': company_id[0]})
        self.render('company.html',
                    countries=pycountry.countries,
                    user=user_info,
                    employees=employees)


class Contact(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        user_info = yield self.get_user()
        companies = yield self.get_companies()
        self.render('contact.html', companies=companies, user=user_info)

    @gen.coroutine
    @tornado.web.authenticated
    def post(self):
        user_info = yield self.get_user()
        companies = yield self.get_companies()
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
        companies = yield self.get_companies()
        self.render('notification.html', companies=companies, user=user_info)

    @gen.coroutine
    @tornado.web.authenticated
    def post(self):
        user_info = yield self.get_user()
        companies = yield self.get_companies()
        self.render('notification.html', companies=companies, user=user_info)


class Note(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        user_info = yield self.get_user()
        companies = yield self.get_companies()
        self.render('note.html',
                    companies=companies,
                    contacts=contacts,
                    notes=notes,
                    user=user_info)

    @gen.coroutine
    @tornado.web.authenticated
    def post(self):
        user_info = yield self.get_user()
        companies = yield self.get_companies()
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
