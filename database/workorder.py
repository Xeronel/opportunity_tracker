from .base import QueryGroup
from tornado import gen
import psycopg2


class WorkOrder(QueryGroup):
    def __index__(self, db):
        super(WorkOrder, self).__init__(db)

    @gen.coroutine
    def get(self, work_order):
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
    def create(self, station, creator):
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

    @staticmethod
    def _value_builder(values, arg_count):
        query_len, remainder = divmod(len(values), arg_count)
        if remainder != 0:
            raise ValueError('Values must be evenly divisible by the number of arguments')
        args = ('%s, ' * arg_count)[:-2]
        return (('(%s), ' % args) * query_len)[:-2]
