import psycopg2
import momoko
import config
from tornado import gen
from datetime import date
from decimal import Decimal


class Database:
    def __init__(self, ioloop):
        self.request = None
        self.pool = momoko.Pool(dsn="dbname=%s user=%s password=%s host=%s port=%s" %
                                    (config.db.database, config.db.username, config.db.password,
                                     config.db.hostname, config.db.port),
                                size=1,
                                max_size=config.db.max_size,
                                auto_shrink=config.db.auto_shrink,
                                ioloop=ioloop)

    def connect(self):
        return self.pool.connect()

    @gen.coroutine
    def execute(self, *args, **kwargs):
        # Throws momoko.PartiallyConnectedError if database is down
        try:
            cursor = yield self.pool.execute(*args, **kwargs)
        except psycopg2.OperationalError:
            yield self.connect()
            cursor = yield self.pool.execute(*args, **kwargs)
        return cursor

    @gen.coroutine
    def get_stations(self):
        cursor = yield self.execute("SELECT * FROM wire_station")
        return cursor.fetchall()

    @gen.coroutine
    def get_employees(self):
        cursor = yield self.execute("SELECT id, first_name, last_name FROM employee "
                                    "ORDER BY first_name ASC, last_name ASC;")
        return cursor.fetchall()

    @gen.coroutine
    def get_companies(self, uid=None):
        if uid:
            cursor = yield self.execute("SELECT id, name FROM company "
                                        "WHERE employee = %s;",
                                        [uid])
        else:
            cursor = yield self.execute("SELECT id, name FROM company;")
        return cursor.fetchall()

    @gen.coroutine
    def get_uoms(self):
        cursor = yield self.execute("SELECT uom "
                                    "FROM unit_of_measure")
        return cursor.fetchall()

    @gen.coroutine
    def get_part_types(self):
        cursor = yield self.execute("SELECT part_type "
                                    "FROM part_type")
        return cursor.fetchall()

    @gen.coroutine
    def get_part_numbers(self, part_type=None):
        if part_type:
            cursor = yield self.execute("SELECT * FROM part WHERE part_type = %s;",
                                        [part_type])
        else:
            cursor = yield self.execute("SELECT * FROM part;")
        return self.parse_query(cursor.fetchall(), cursor.description)

    def parse_query(self, data, description, convert_decimal=True):
        if type(data) == list:
            result = []
            for value in data:
                result.append(self.parse_query(value, description))
        elif type(data) == tuple:
            result = {}
            for i in range(len(description)):
                if type(data[i]) == date:
                    value = data[i].strftime('%Y-%m-%d')
                elif type(data[i]) == Decimal and convert_decimal:
                    value = str(data[i])
                else:
                    value = data[i]
                result[description[i].name] = value
        else:
            result = {}
        return result
