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
        rpc = {'get_location': self.get_location}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))

    @gen.coroutine
    def get_location(self, company_id):
        cursor = yield self.db.execute(
            "SELECT id, company, address1, address2, city, state, postal_code, country "
            "FROM location WHERE id = %(id)s",
            {'id': company_id})
        data = cursor.fetchone()
        result = {}
        if data:
            for i in range(len(cursor.description)):
                result[cursor.description[i].name] = data[i]
        return result
