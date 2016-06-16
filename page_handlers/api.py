from .base import BaseHandler
import tornado.web
import tornado.escape
from tornado.escape import json_encode
from tornado import gen
import pycountry
import psycopg2


class Company(BaseHandler):
    @gen.coroutine
    def get(self, proc, arg):
        rpc = {'get_location': self.get_location,
               'get_company': self.get_company}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))

    @gen.coroutine
    def get_location(self, company_id):
        if company_id:
            cursor = yield self.db.execute(
                "SELECT id, company, address1, address2, city, state, postal_code, country "
                "FROM location WHERE company = %(id)s",
                {'id': company_id})
            return self.parse_query(cursor.fetchone(), cursor.description)
        else:
            return {}

    @gen.coroutine
    def get_company(self, company_id):
        if company_id:
            cursor = yield self.db.execute(
                "SELECT id, name, active, employee, creator FROM company WHERE id = %s",
                [company_id]
            )
            return self.parse_query(cursor.fetchone(), cursor.description)
        else:
            return {}

    @staticmethod
    def parse_query(data, description):
        result = {}
        if data:
            for i in range(len(description)):
                result[description[i].name] = data[i]
        return result
