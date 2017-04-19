import psycopg2
import momoko
import config
from tornado import gen
from datetime import date, datetime
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
    def get_wire_stations(self):
        cursor = yield self.execute("SELECT * FROM wire_station")
        return self.parse_query(cursor.fetchall(), cursor.description)

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

    @gen.coroutine
    def create_work_order(self, station, creator):
        """
        Create a work order and return it's id
        :param station: Station id
        :param creator: User id
        :return: Work order id
        """
        cursor = yield self.execute(
            "INSERT INTO work_order (station, creator) "
            "VALUES (%s, %s) "
            "RETURNING id;",
            [station, creator]
        )
        return cursor.fetchone()[0]

    @gen.coroutine
    def get_work_order(self, work_order):
        cursor1 = self.pool.execute("""
        SELECT station, complete, creator, created
        FROM work_order
        WHERE id = %s
        """, [work_order])
        cursor2 = self.pool.execute("""
        SELECT
            woi.id, woi.part_number, woi.qty, woi.remaining, woi.cut_length, kit_bom.part_number AS reel_part_number
        FROM
            work_order_items woi
        JOIN
            kit_bom
        ON
            woi.part_number = kit_bom.kit_part_number
        WHERE
            woi.work_order = %s AND
            woi.remaining > 0
        """, [work_order])
        cursor3 = self.pool.execute("""
        SELECT id, part_number, reel_length, current_length
        FROM work_order_reels
        WHERE work_order = %s
        """, [work_order])

        try:
            yield [cursor1, cursor2, cursor3]
        except psycopg2.OperationalError:
            yield self.connect()
            yield [cursor1, cursor2, cursor3]

        wo, wo_items, wo_reels = cursor1.result(), cursor2.result(), cursor3.result()
        return {'work_order': self.parse_query(wo.fetchone(), wo.description),
                'reels': self.parse_query(wo_reels.fetchall(), wo_reels.description),
                'items': self.parse_query(wo_items.fetchall(), wo_items.description)}

    @gen.coroutine
    def get_active_work_order(self, station_name):
        cursor = yield self.execute("""
        SELECT active_work_order
        FROM wire_station
        WHERE name = %s
        """, [station_name.upper()])
        return self.parse_query(cursor.fetchone(), cursor.description)

    @gen.coroutine
    def get_wire_station(self, station_name):
        cursor = yield self.execute("""
        SELECT *
        FROM wire_station
        WHERE name = %s
        """, [station_name.upper()])
        return self.parse_query(cursor.fetchone(), cursor.description)

    @gen.coroutine
    def add_reels(self, work_order, reels):
        """
        Add reels to a work order
        :param work_order: Work order id
        :param reels: List of reel objects
        """
        reel_list = []
        for reel in reels:
            for i in range(reel['qty']):
                reel_list.append(reel['part_number'])
                reel_list.append(reel['length'])
                reel_list.append(work_order)

        yield self.execute(
            "INSERT INTO work_order_reels (part_number, reel_length, work_order) "
            "VALUES %s" % self._value_builder(reel_list, 3),
            reel_list
        )

    @gen.coroutine
    def get_reels(self, work_order):
        cursor = yield self.execute("""
        SELECT id, part_number, reel_length, current_length
        FROM work_order_reels
        WHERE work_order = %s
        """, [work_order])
        return self.parse_query(cursor.fetchall(), cursor.description)

    @gen.coroutine
    def add_items(self, work_order, cuts):
        """
        Add cuts to a work order
        :param work_order: 
        :param cuts: 
        :return: 
        """
        cut_list = []
        for cut in cuts:
            cut_list.append(cut['part_number'])
            cut_list.append(cut['qty'])
            cut_list.append(cut['length'])
            cut_list.append(work_order)

        yield self.execute(
            "INSERT INTO work_order_items (part_number, qty, cut_length, work_order) "
            "VALUES %s" % self._value_builder(cut_list, 4),
            cut_list
        )

    @gen.coroutine
    def get_items(self, wo_id):
        cursor = yield self.execute("""
        SELECT
            woi.id, woi.part_number, woi.qty, woi.remaining, woi.cut_length, kit_bom.part_number AS reel_part_number
        FROM
            work_order_items woi
        JOIN
            kit_bom
        ON
            woi.part_number = kit_bom.kit_part_number
        WHERE
            woi.work_order = %s AND
            woi.remaining > 0
        """, [wo_id])
        result = self.parse_query(cursor.fetchall(), cursor.description)
        return result

    def parse_query(self, data, description, convert_decimal=True):
        if type(data) == list:
            result = []
            for value in data:
                result.append(self.parse_query(value, description))
        elif type(data) == tuple:
            result = {}
            for i in range(len(description)):
                if type(data[i]) == date or type(data[i]) == datetime:
                    value = data[i].strftime('%Y-%m-%d')
                elif type(data[i]) == Decimal and convert_decimal:
                    value = str(data[i])
                else:
                    value = data[i]
                result[description[i].name] = value
        else:
            result = {}
        return result

    @staticmethod
    def _value_builder(values, arg_count):
        query_len, remainder = divmod(len(values), arg_count)
        if remainder != 0:
            raise ValueError('Values must be evenly divisible by the number of arguments')
        args = ('%s, ' * arg_count)[:-2]
        return (('(%s), ' % args) * query_len)[:-2]
