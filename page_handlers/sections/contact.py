from page_handlers import BaseHandler
from tornado import gen, web
from tornado.escape import json_encode
import psycopg2


class Contact(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self, form):
        companies = yield self.db.get_companies()
        yield self.render('contact.html',
                          companies=companies,
                          form=form)

    @gen.coroutine
    @web.authenticated
    def post(self, form):
        forms = {'add': self.add_contact,
                 'mod': self.mod_contact,
                 'rem': self.rem_contact}
        if form in forms:
            yield forms[form]()
        else:
            yield self.render_form(form)

    @gen.coroutine
    @web.authenticated
    def add_contact(self):
        company = self.get_argument('company')
        first_name = self.get_argument('firstname')
        last_name = self.get_argument('lastname', '')
        title = self.get_argument('title', '')
        email = self.get_argument('email', '')
        phone = self.get_argument('phone', '')
        ext = self.get_argument('ext', '')

        try:
            yield self.db.execute(
                "INSERT INTO contact (company, first_name, last_name, title, email, phone, ext) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s);",
                [company, first_name, last_name, title, email, phone, ext])
        except psycopg2.IntegrityError:
            pass

        yield self.render_form()

    @gen.coroutine
    @web.authenticated
    def mod_contact(self):
        company = self.get_argument('company')
        contact = self.get_argument('contact')
        first_name = self.get_argument('firstname')
        title = self.get_argument('title')
        last_name = self.get_argument('lastname', '')
        email = self.get_argument('email', '')
        phone = self.get_argument('phone', '')
        ext = self.get_argument('ext', '')

        try:
            yield self.db.execute(
                "UPDATE contact "
                "SET (first_name, last_name, title, email, phone, ext) = (%s, %s, %s, %s, %s, %s) "
                "WHERE id = %s AND company = %s",
                [first_name, last_name, title, email, phone, ext,
                 contact, company])
        except psycopg2.IntegrityError:
            self.send_error(400)
        yield self.render_form()

    @gen.coroutine
    @web.authenticated
    def rem_contact(self):
        contact_id = self.get_argument('contact')
        yield self.db.execute("DELETE FROM contact WHERE id = %s;",
                              [contact_id])
        yield self.render_form()

    @gen.coroutine
    @web.authenticated
    def render_form(self, form=None, companies=None):
        if not form:
            form = self.request.uri.strip('/')[:3]
        if not companies:
            companies = yield self.db.get_companies()

        yield self.render('contact.html',
                          companies=companies,
                          form=form)


class GetContacts(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self, company):
        if company:
            cursor = yield self.db.execute(
                "SELECT id, first_name, last_name FROM contact "
                "WHERE company = %s", [company])
            contacts = cursor.fetchall()
            if len(contacts) > 0:
                contacts.append(('', 'None', ''))
                self.write(json_encode([{'text': '%s %s' % (first, last), 'value': idx}
                                        for idx, first, last in contacts]))
            else:
                self.write('')
        else:
            self.write('')
