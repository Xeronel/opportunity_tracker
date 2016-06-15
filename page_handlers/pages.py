from .base import BaseHandler
import tornado.web
import tornado.escape
from tornado.escape import json_encode
from tornado import gen
import pycountry
import psycopg2
from datetime import datetime


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
    def get(self, form):
        user_info = yield self.get_user()
        employees = yield self.get_employees()
        companies = yield self.get_companies()
        self.render('company.html',
                    countries=pycountry.countries,
                    user=user_info,
                    employees=employees,
                    companies=companies,
                    form=form)

    @gen.coroutine
    @tornado.web.authenticated
    def post(self, form):
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
                                       "RETURNING id;",
                                       {'company_name': company_name,
                                        'active': True,
                                        'employee': employee,
                                        'creator': user_info.uid})
        company_id = cursor.fetchone()
        yield self.db.execute(
            "INSERT INTO location (address1, address2, city, state, country, postal_code, company) "
            "VALUES (%(address1)s, %(address2)s, %(city)s, %(state)s, %(country)s, %(postal_code)s, %(company)s);",
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
                    employees=employees,
                    form=form)


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
        company = self.get_argument('company')
        first_name = self.get_argument('firstname')
        last_name = self.get_argument('lastname')
        title = self.get_argument('title')
        email = self.get_argument('email')
        phone = self.get_argument('phone')

        try:
            yield self.db.execute(
                "INSERT INTO contact (company, first_name, last_name, title, email, phone) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                [company, first_name, last_name, title, email, phone])
        except psycopg2.IntegrityError:
            pass

        user_info = yield self.get_user()
        companies = yield self.get_companies()
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
        company = self.get_argument('company')
        notify_date = datetime.strptime(self.get_argument('date'), '%m-%d-%Y')
        note = self.get_argument('note')
        uid = self.get_secure_cookie('uid').decode('utf-8')
        yield self.db.execute("INSERT INTO notification (company, notify_date, note, employee) "
                              "VALUES (%s, %s, %s, %s)",
                              [company, notify_date.strftime('%Y-%m-%d'), note, uid])
        self.render('notification.html', companies=companies, user=user_info)


class Note(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        user_info = yield self.get_user()
        companies = yield self.get_companies()
        self.render('note.html',
                    companies=companies,
                    user=user_info)

    @gen.coroutine
    @tornado.web.authenticated
    def post(self):
        company = self.get_argument('company')
        action = self.get_argument('action')
        note = self.get_argument('note')
        date = datetime.strptime(self.get_argument('date'), '%m-%d-%Y')
        try:
            contact = int(self.get_argument('contact'))
        except ValueError:
            raise tornado.web.HTTPError(400, 'contact must be an integer')

        # Store note
        yield self.db.execute(
            "INSERT INTO notes (contact, company, action, note_date, note) "
            "VALUES (%s, %s, %s, %s, %s);",
            [contact, company, action, date, note])

        user_info = yield self.get_user()
        companies = yield self.get_companies()
        self.render('note.html',
                    companies=companies,
                    user=user_info)


class GetNotes(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self, company):
        # Get the last 5 notes within the past 90 days
        cursor = yield self.db.execute("SELECT note_date, action, first_name, last_name, note "
                                       "FROM notes, contact "
                                       "WHERE notes.company = %s "
                                       "AND contact.id = notes.contact "
                                       "AND notes.note_date > NOW() - INTERVAL '90 days' "
                                       "ORDER BY note_date DESC "
                                       " LIMIT 5;",
                                       [company])
        notes = cursor.fetchall()
        if len(notes) > 0:
            user_info = yield self.get_user()
            self.render('get_notes.html',
                        notes=notes,
                        user=user_info)
        else:
            self.write('')


class GetContacts(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self, company):
        cursor = yield self.db.execute(
            "SELECT id, first_name, last_name FROM contact "
            "WHERE company = %s", company)
        contacts = cursor.fetchall()
        if len(contacts) > 0:
            self.write(json_encode([{'text': '%s %s' % (first, last), 'value': idx}
                                    for idx, first, last in contacts]))
        else:
            self.write('')


class ClearCompany(BaseHandler):
    def get(self):
        self.clear_cookie('company')
