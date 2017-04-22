from .base import BaseHandler
from tornado import web
from tornado.escape import json_encode
from tornado import gen
from dateutil import parser as dateutil
from inspect import signature
import psycopg2
import traceback


class ApiBase(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(ApiBase, self).__init__(*args, **kwargs)
        self.rpc = {}

    @gen.coroutine
    @web.authenticated
    def get(self, arg, proc=''):
        if proc in self.rpc:
            if len(signature(self.rpc[proc]).parameters) > 0:
                try:
                    result = yield self.rpc[proc](arg)
                except psycopg2.Error:
                    traceback.print_exc()
                    result = {}
            else:
                result = yield self.rpc[proc]()
            self.write(json_encode(result))
        else:
            self.write(json_encode({}))

    def _start_date(self):
        start_date = self.get_argument('start_date', False)
        if start_date:
            start_date = dateutil.parse(start_date).strftime('%Y-%m-%d')
        return start_date

    def _end_date(self):
        end_date = self.get_argument('end_date', False)
        if end_date:
            end_date = dateutil.parse(end_date).strftime('%Y-%m-%d')
        return end_date


class Company(ApiBase):
    @gen.coroutine
    @web.authenticated
    def get(self, arg, proc=''):
        rpc = {'': self.company,
               'location': self.location,
               'notes': self.notes,
               'employee': self.employee,
               'notifications': self.notifications,
               'projects': self.projects}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))
        else:
            self.write(json_encode({}))

    @gen.coroutine
    @web.authenticated
    def post(self, arg, proc=''):
        rpc = {'': self.company,
               'location': self.location,
               'notes': self.notes,
               'employee': self.employee,
               'notifications': self.notifications}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))
        else:
            self.write(json_encode({}))

    @gen.coroutine
    @web.authenticated
    def location(self, company_id):
        if company_id:
            cursor = yield self.db.execute(
                "SELECT id, company, address1, address2, city, state, postal_code, country "
                "FROM location WHERE company = %(id)s",
                {'id': company_id})
            return self.db.parse_query(cursor.fetchone(), cursor.description)
        else:
            return {}

    @gen.coroutine
    @web.authenticated
    def company(self, company_id):
        if company_id:
            cursor = yield self.db.execute(
                "SELECT id, name, active, employee, creator FROM company WHERE id = %s",
                [company_id]
            )
            return self.db.parse_query(cursor.fetchone(), cursor.description)
        else:
            return {}

    @gen.coroutine
    @web.authenticated
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
            return self.db.parse_query(cursor.fetchall(), cursor.description)
        else:
            return {}

    @gen.coroutine
    @web.authenticated
    def employee(self, company_id):
        if company_id:
            cursor = yield self.db.execute(
                "SELECT employee FROM company WHERE id = %s",
                [company_id]
            )
            return self.db.parse_query(cursor.fetchone(), cursor.description)
        else:
            return {}

    @gen.coroutine
    @web.authenticated
    def notifications(self, company_id):
        if company_id:
            start_date = self._start_date()
            end_date = self._end_date()
            if start_date and end_date:
                cursor = yield self.db.execute(
                    "SELECT company.name, first_name, last_name, note, notify_date, sent "
                    "FROM notification "
                    "INNER JOIN company "
                    "ON company.id = notification.company "
                    "INNER JOIN employee "
                    "ON notification.employee = employee.id "
                    "WHERE notification.company=%s "
                    "AND notify_date >= %s "
                    "AND notify_date <= %s;",
                    [company_id, start_date, end_date]
                )
            else:
                cursor = yield self.db.execute(
                    "SELECT company.name, first_name, last_name, note, notify_date, sent "
                    "FROM notification "
                    "INNER JOIN company "
                    "ON company.id = notification.company "
                    "INNER JOIN employee "
                    "ON notification.employee = employee.id "
                    "WHERE notification.company=%s;",
                    [company_id])
            return self.db.parse_query(cursor.fetchall(), cursor.description)
        else:
            return {}

    @gen.coroutine
    def projects(self, company_id):
        if company_id:
            cursor = yield self.db.execute(
                "SELECT * FROM project "
                "WHERE company = %s",
                [company_id]
            )
            return self.db.parse_query(cursor.fetchall(), cursor.description)
        else:
            return {}


class Contact(ApiBase):
    @gen.coroutine
    @web.authenticated
    def get(self, arg, proc=''):
        rpc = {'': self.contact}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))
        else:
            self.write(json_encode({}))

    @gen.coroutine
    @web.authenticated
    def contact(self, contact_id):
        if contact_id:
            cursor = yield self.db.execute("SELECT * FROM contact "
                                           "WHERE id = %s;",
                                           [contact_id])
            return self.db.parse_query(cursor.fetchone(), cursor.description)
        else:
            return {}


class Employee(ApiBase):
    @gen.coroutine
    @web.authenticated
    def get(self, arg, proc=''):
        rpc = {'companies': self.companies,
               'notes': self.notes,
               'notifications': self.notifications}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))
        else:
            self.write(json_encode({}))

    @gen.coroutine
    @web.authenticated
    def post(self, arg, proc=''):
        rpc = {'companies': self.companies,
               'notes': self.notes}
        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))
        else:
            self.write(json_encode({}))

    @gen.coroutine
    @web.authenticated
    def companies(self, employee_id):
        if employee_id:
            cursor = yield self.db.execute("SELECT * FROM company "
                                           "WHERE employee = %s;",
                                           [employee_id])
            return self.db.parse_query(cursor.fetchall(), cursor.description)
        else:
            return {}

    @gen.coroutine
    @web.authenticated
    def notes(self, employee_id):
        if employee_id:
            start_date = self._start_date()
            end_date = self._end_date()
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
            return self.db.parse_query(cursor.fetchall(), cursor.description)
        else:
            return {}

    @gen.coroutine
    @web.authenticated
    def notifications(self, employee_id):
        if employee_id:
            start_date = self._start_date()
            end_date = self._end_date()
            if start_date and end_date:
                cursor = yield self.db.execute(
                    "SELECT company.name, first_name, last_name, note, notify_date, sent "
                    "FROM notification "
                    "INNER JOIN company "
                    "ON company.id = notification.company "
                    "INNER JOIN employee "
                    "ON notification.employee = employee.id "
                    "WHERE notification.employee=%s "
                    "AND notify_date >= %s "
                    "AND notify_date <= %s;",
                    [employee_id, start_date, end_date]
                )
            else:
                cursor = yield self.db.execute(
                    "SELECT company.name, first_name, last_name, note, notify_date, sent "
                    "FROM notification "
                    "INNER JOIN company "
                    "ON company.id = notification.company "
                    "INNER JOIN employee "
                    "ON notification.employee = employee.id "
                    "WHERE notification.employee=%s;",
                    [employee_id]
                )
            return self.db.parse_query(cursor.fetchall(), cursor.description)
        else:
            return {}


class Part(ApiBase):
    @gen.coroutine
    @web.authenticated
    def get(self, arg, proc=''):
        rpc = {'': self.part,
               'components': self.components}

        if proc in rpc:
            result = yield rpc[proc](arg)
            self.write(json_encode(result))
        else:
            self.write(json_encode({}))

    @gen.coroutine
    def part(self, part_number):
        if part_number == 'parts':
            cursor = yield self.db.execute("SELECT * FROM part;")
            return self.db.parse_query(cursor.fetchall(), cursor.description)
        elif part_number:
            cursor = yield self.db.execute(
                "SELECT * FROM part WHERE part_number = %s;",
                [part_number.upper()]
            )
            return self.db.parse_query(cursor.fetchone(), cursor.description)
        else:
            return {}

    @gen.coroutine
    def components(self, part_number):
        if part_number:
            cursor = yield self.db.execute("SELECT * FROM kit_bom WHERE kit_part_number = %s", [part_number])
            return self.db.parse_query(cursor.fetchall(), cursor.description)


class WorkOrder(ApiBase):
    def __init__(self, *args, **kwargs):
        super(WorkOrder, self).__init__(*args, **kwargs)
        self.rpc = {'': self.db.work_order.get_all,
                    'items': self.db.work_order.get_items}


class Station(ApiBase):
    def __init__(self, *args, **kwargs):
        super(Station, self).__init__(*args, **kwargs)
        self.rpc = {
            '': self.get_station,
            'active_work_order': self.db.station.get_active
        }

    @gen.coroutine
    def get_station(self, employee=None):
        if not employee:
            employee = self.get_secure_cookie('uid').decode()
            result = yield self.db.station.get(employee)
            return result
        else:
            result = yield self.db.station.get(employee)
            return result
