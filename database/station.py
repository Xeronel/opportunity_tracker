from tornado import gen
from .base import QueryGroup


class Station(QueryGroup):
    def __init__(self, db):
        super(Station, self).__init__(db)

    @gen.coroutine
    def get_all(self):
        cursor = yield self.execute("""
        SELECT
          station.id,
          station.location,
          employee.first_name,
          employee.last_name,
          station.employee,
          station.active_work_order,
          station.ip_address
        FROM
          station
        JOIN
          employee
        ON
          station.employee = employee.id
        """)
        return self.parse_query(cursor.fetchall(), cursor.description)

    @gen.coroutine
    def get_active(self, station_id):
        cursor = yield self.execute("""
        SELECT active_work_order
        FROM station
        WHERE id = %s
        """, [station_id])
        return self.parse_query(cursor.fetchone(), cursor.description)

    @gen.coroutine
    def get(self, employee):
        cursor = yield self.execute("""
        SELECT *
        FROM station
        WHERE employee = %s
        """, [employee])
        return self.parse_query(cursor.fetchone(), cursor.description)
