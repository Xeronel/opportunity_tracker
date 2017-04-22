from page_handlers import BaseHandler
from tornado import gen, web
from subprocess import call
from os import devnull
import traceback
import psycopg2


class WorkOrder(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self, form):
        yield self.render(form)

    @gen.coroutine
    @web.authenticated
    def post(self, form):
        try:
            user = yield self.get_user()
            station = self.get_json_arg('station')
            reels = self.get_json_arg('reels')
            cuts = self.get_json_arg('cuts')

            # Create a new work order
            wo_id = yield self.db.work_order.create(station, user.uid)
            yield [self.db.work_order.add_reels(wo_id, reels), self.db.work_order.add_items(wo_id, cuts)]
        except psycopg2.IntegrityError as e:
            self.send_error(400, reason=e.pgerror.replace('\n', ' ').rstrip())
            traceback.print_exc()
        else:
            self.clear()
            self.set_status(200, 'OK')
            self.finish('Created work order: %s' % wo_id)

    @gen.coroutine
    @web.authenticated
    def render(self, form, **kwargs):
        reels = yield self.db.get_part_numbers('ITEM')
        cuts = yield self.db.get_part_numbers('KIT')
        stations = yield self.db.station.get_all()
        yield super(WorkOrder, self).render('warehouse.html',
                                            stations=stations,
                                            reels=reels,
                                            cuts=cuts,
                                            form=form)


class Print(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self):
        yield self.render('print.html')

    @gen.coroutine
    @web.authenticated
    def post(self):
        qty = self.get_argument('qty')
        top_left = self.get_argument('topleft', '')
        left_center = self.get_argument('leftcenter', '')
        bottom_left = self.get_argument('bottomleft', '')
        call(['/usr/bin/python2', '/opt/opportunity_tracker/print_label.py', top_left, left_center, bottom_left, qty],
             stdout=open(devnull, 'w'),
             close_fds=True)
        yield self.render('print.html')
