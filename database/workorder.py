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
            woi.id, woi.part_number, woi.qty, woi.remaining, woi.consume_qty, kit_bom.part_number AS consumable_part_number
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
        SELECT id, part_number, qty, current_qty
        FROM work_order_consumable
        WHERE work_order = %s
        """, [work_order])

        try:
            yield [cursor1, cursor2, cursor3]
        except psycopg2.OperationalError:
            yield self.connect()
            yield [cursor1, cursor2, cursor3]

        wo, wo_items, wo_consumables = cursor1.result(), cursor2.result(), cursor3.result()
        return {'work_order': self.parse_query(wo.fetchone(), wo.description),
                'consumables': self.parse_query(wo_consumables.fetchall(), wo_consumables.description),
                'items': self.parse_query(wo_items.fetchall(), wo_items.description)}

    @gen.coroutine
    def get_all(self):
        cursor = yield self.execute("SELECT * FROM work_order")
        return self.parse_query(cursor.fetchall(), cursor.description)

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
    def add_consumables(self, work_order, consumables):
        """
        Add consumables to a work order
        :param work_order: Work order id
        :param consumables: List of consumable objects
        """
        consumable_list = []
        for consumable in consumables:
            for i in range(consumable['qty']):
                consumable_list.append(consumable['part_number'])
                consumable_list.append(consumable['length'])
                consumable_list.append(work_order)

        yield self.execute(
            "INSERT INTO work_order_consumable (part_number, qty, work_order) "
            "VALUES %s" % self._value_builder(consumable_list, 3),
            consumable_list
        )

    @gen.coroutine
    def get_consumables(self, work_order):
        cursor = yield self.execute("""
        SELECT id, part_number, qty, current_qty
        FROM work_order_consumable
        WHERE work_order = %s
        """, [work_order])
        return self.parse_query(cursor.fetchall(), cursor.description)

    @gen.coroutine
    def add_items(self, work_order, items):
        """
        Add items to a work order
        :param work_order: 
        :param items: 
        :return: 
        """
        item_list = []
        for item in items:
            item_list.append(item['part_number'])
            item_list.append(item['qty'])
            item_list.append(item['length'])
            item_list.append(work_order)

        yield self.execute(
            "INSERT INTO work_order_items (part_number, qty, consume_qty, work_order) "
            "VALUES %s" % self._value_builder(item_list, 4),
            item_list
        )

    @gen.coroutine
    def get_items(self, wo_id):
        cursor = yield self.execute("""
        SELECT
            woi.id,
            woi.part_number,
            woi.qty,
            woi.remaining,
            woi.consume_qty,
            kit_bom.part_number AS consumable_part
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
