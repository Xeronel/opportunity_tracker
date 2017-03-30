from page_handlers import BaseHandler
from tornado import gen, web
from subprocess import call
from os import devnull
import traceback
import psycopg2


class Warehouse(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self, form):
        yield self.render(form)

    @gen.coroutine
    @web.authenticated
    def post(self, form):
        try:
            station = self.get_json_arg('wire_station')
            user = yield self.get_user()
            reels = self.get_json_arg('reels')
            wo_id = yield self.db.create_work_order(station, user.uid)
        except (TypeError, ValueError, KeyError, IndexError, web.MissingArgumentError):
            self.send_error(400)
        except psycopg2.IntegrityError as e:
            self.send_error(400, reason=e.pgerror.replace('\n', ' ').rstrip())
            traceback.print_exc()
        self.clear()
        self.set_status(200, 'OK')
        self.finish('success')

    @gen.coroutine
    @web.authenticated
    def render(self, form, **kwargs):
        reels = yield self.db.get_part_numbers('ITEM')
        cuts = yield self.db.get_part_numbers('KIT')
        stations = yield self.db.get_wire_stations()
        yield super(Warehouse, self).render('warehouse.html',
                                            wire_stations=stations,
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
