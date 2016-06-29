from .base import BaseHandler
import tornado.web
import tornado.escape
from tornado.escape import json_encode
from tornado import gen
from dateutil import parser as dateutil


class Company(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self, arg, proc=''):
        rpc = {'': self.company,
               'location': self.location,
               'notes': self.notes,
               'employee': self.employee}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))
        else:
            self.write(json_encode({}))

    @gen.coroutine
    @tornado.web.authenticated
    def post(self, arg, proc=''):
        rpc = {'': self.company,
               'location': self.location,
               'notes': self.notes,
               'employee': self.employee}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))
        else:
            self.write(json_encode({}))

    @gen.coroutine
    @tornado.web.authenticated
    def location(self, company_id):
        if company_id:
            cursor = yield self.db.execute(
                "SELECT id, company, address1, address2, city, state, postal_code, country "
                "FROM location WHERE company = %(id)s",
                {'id': company_id})
            return self.parse_query(cursor.fetchone(), cursor.description)
        else:
            return {}

    @gen.coroutine
    @tornado.web.authenticated
    def company(self, company_id):
        if company_id:
            cursor = yield self.db.execute(
                "SELECT id, name, active, employee, creator FROM company WHERE id = %s",
                [company_id]
            )
            return self.parse_query(cursor.fetchone(), cursor.description)
        else:
            return {}

    @gen.coroutine
    @tornado.web.authenticated
    def notes(self, company_id):
        if company_id:
            start_date = self.get_argument('start_date', False)
            if start_date:
                start_date = dateutil.parse(start_date).strftime('%Y-%m-%d')

            end_date = self.get_argument('end_date', False)
            if end_date:
                end_date = dateutil.parse(end_date).strftime('%Y-%m-%d')

            if start_date and end_date:
                cursor = yield self.db.execute(
                    "SELECT name, note_date, note_type, first_name, last_name, note "
                    "FROM notes "
                    "INNER JOIN company "
                    "ON company.id = notes.company "
                    "LEFT OUTER JOIN contact "
                    "ON (notes.contact = contact.id) "
                    "WHERE notes.company = %s "
                    "AND note_date >= %s "
                    "AND note_date <= %s;",
                    [company_id, start_date, end_date]
                )
            else:
                cursor = yield self.db.execute(
                    "SELECT name, note_date, note_type, first_name, last_name, note "
                    "FROM notes "
                    "INNER JOIN company "
                    "ON company.id = notes.company "
                    "LEFT OUTER JOIN contact "
                    "ON (notes.contact = contact.id) "
                    "WHERE notes.company = %s;",
                    [company_id]
                )
            return self.parse_query(cursor.fetchall(), cursor.description)
        else:
            return {}

    @gen.coroutine
    @tornado.web.authenticated
    def employee(self, company_id):
        if company_id:
            cursor = yield self.db.execute(
                "SELECT employee FROM company WHERE id = %s",
                [company_id]
            )
            return self.parse_query(cursor.fetchone(), cursor.description)
        else:
            return {}


class Contact(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self, arg, proc=''):
        rpc = {'': self.contact}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))
        else:
            self.write(json_encode({}))

    @gen.coroutine
    @tornado.web.authenticated
    def contact(self, contact_id):
        if contact_id:
            cursor = yield self.db.execute("SELECT * FROM contact "
                                           "WHERE id = %s;",
                                           [contact_id])
            return self.parse_query(cursor.fetchone(), cursor.description)
        else:
            return {}


class Employee(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self, arg, proc=''):
        rpc = {'companies': self.companies,
               'notes': self.notes}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))
        else:
            self.write(json_encode({}))

    @gen.coroutine
    @tornado.web.authenticated
    def post(self, arg, proc=''):
        rpc = {'companies': self.companies,
               'notes': self.notes}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))
        else:
            self.write(json_encode({}))

    @gen.coroutine
    @tornado.web.authenticated
    def companies(self, employee_id):
        if employee_id:
            cursor = yield self.db.execute("SELECT * FROM company "
                                           "WHERE employee = %s;",
                                           [employee_id])
            return self.parse_query(cursor.fetchall(), cursor.description)
        else:
            return {}

    @gen.coroutine
    @tornado.web.authenticated
    def notes(self, employee_id):
        if employee_id:
            start_date = self.get_argument('start_date', False)
            if start_date:
                start_date = dateutil.parse(start_date).strftime('%Y-%m-%d')

            end_date = self.get_argument('end_date', False)
            if end_date:
                end_date = dateutil.parse(end_date).strftime('%Y-%m-%d')

            if start_date and end_date:
                cursor = yield self.db.execute(
                    "SELECT name, note_date, note_type, first_name, last_name, note "
                    "FROM notes "
                    "INNER JOIN company "
                    "ON company.id = notes.company "
                    "LEFT OUTER JOIN contact "
                    "ON notes.contact = contact.id "
                    "WHERE employee=%s "
                    "AND note_date >= %s "
                    "AND note_date <= %s;",
                    [employee_id, start_date, end_date]
                )
            else:
                cursor = yield self.db.execute(
                    "SELECT name, note_date, note_type, first_name, last_name, note "
                    "FROM notes "
                    "INNER JOIN company "
                    "ON company.id = notes.company "
                    "LEFT OUTER JOIN contact "
                    "ON notes.contact = contact.id "
                    "WHERE employee=%s;",
                    [employee_id]
                )
            return self.parse_query(cursor.fetchall(), cursor.description)
        else:
            return {}
