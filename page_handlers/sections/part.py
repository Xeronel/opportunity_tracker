from page_handlers import BaseHandler
from tornado import gen, web
import traceback
import psycopg2


class Part(BaseHandler):
    form = None

    @gen.coroutine
    @web.authenticated
    def get(self, form):
        self.form = form
        yield self.render_form()

    @gen.coroutine
    @web.authenticated
    def post(self, form):
        self.form = form
        forms = {'add': self.add_part,
                 'mod': self.modify_part,
                 'rem': self.remove_part}

        if form in forms:
            yield forms[form]()
        else:
            yield self.render('part.html')

    @gen.coroutine
    def add_part(self):
        try:
            part_number = self.get_json_arg('part_number').upper()
            description = self.get_json_arg('description').upper()
            unit_of_measure = self.get_json_arg('uom').upper()
            part_type = self.get_json_arg('part_type').upper()
            cost = self.get_json_arg('cost')
            yield self.db.execute(
                "INSERT INTO part (part_number, description, uom, part_type, cost) "
                "VALUES (%s, %s, %s, %s, %s);",
                [part_number, description, unit_of_measure, part_type, cost])
            if part_type == 'KIT':
                kit_bom = self.get_json_arg('bill_of_materials')
                if len(kit_bom) > 1000:
                    raise ValueError

                if len(kit_bom) > 1:
                    values = ('(%s, %s, %s), ' * len(kit_bom))[:-2]
                else:
                    values = '(%s, %s, %s)'

                kit_items = []
                for kit in kit_bom:
                    kit_items.append(part_number)
                    kit_items.append(kit['part_number'])
                    kit_items.append(kit['qty'])

                yield self.db.execute(
                    "INSERT INTO kit_bom (kit_part_number, part_number, qty) "
                    "VALUES %s;" % values,
                    kit_items
                )
        except (TypeError, ValueError, KeyError, IndexError, web.MissingArgumentError):
            self.send_error(400)
        except psycopg2.IntegrityError as e:
            self.send_error(400, reason=e.pgerror.replace('\n', ' ').rstrip())
            traceback.print_exc()
        else:
            self.clear()
            self.set_status(200, 'OK')
            self.finish('success')

    @gen.coroutine
    def modify_part(self):
        yield self.render_form()

    @gen.coroutine
    def remove_part(self):
        part_number = self.get_argument('part_number')
        yield self.db.execute("DELETE FROM part WHERE part_number = %s", [part_number])
        yield self.render_form()

    @gen.coroutine
    def render_form(self, companies=None, user=None, **kwargs):
        if companies is None:
            companies = yield self.db.get_companies()
        if user is None:
            user = yield self.get_user()
        uoms = yield self.db.get_uoms()
        part_types = yield self.db.get_part_types()
        part_numbers = yield self.db.get_part_numbers()

        yield self.render('part.html',
                          form=self.form,
                          companies=companies,
                          part_types=part_types,
                          part_numbers=part_numbers,
                          uoms=uoms,
                          user=user,
                          **kwargs)
