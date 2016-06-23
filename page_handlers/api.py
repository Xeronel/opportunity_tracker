from .base import BaseHandler
import tornado.web
import tornado.escape
from tornado.escape import json_encode
from tornado import gen
import pycountry
import psycopg2


class Company(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self, proc, arg):
        rpc = {'location': self.location,
               'get_company': self.get_company,
               'notes': self.notes}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))

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
    def get_company(self, company_id):
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
            cursor = yield self.db.execute(
                "SELECT note_date, note_type, first_name, last_name, note "
                "FROM notes "
                "LEFT OUTER JOIN contact "
                "ON (notes.contact = contact.id) "
                "WHERE notes.company = %s;",
                [company_id]
            )
            return self.parse_query(cursor.fetchall(), cursor.description)
        else:
            return {}


class Contact(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self, proc, arg):
        rpc = {'get_contact': self.get_contact}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))

    @gen.coroutine
    @tornado.web.authenticated
    def get_contact(self, contact_id):
        if contact_id:
            cursor = yield self.db.execute("SELECT * FROM contact WHERE id = %s", [contact_id])
            return self.parse_query(cursor.fetchone(), cursor.description)
        else:
            return {}
