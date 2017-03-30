from page_handlers import BaseHandler
from tornado import gen, web
from datetime import datetime


class Note(BaseHandler):
    form = None

    @gen.coroutine
    @web.authenticated
    def get(self, form):
        self.form = form
        companies = yield self.db.get_companies()
        employees = yield self.db.get_employees()
        yield self.render('note.html',
                          companies=companies,
                          employees=employees,
                          form=form)

    @gen.coroutine
    @web.authenticated
    def post(self, form):
        self.form = form
        forms = {'add': self.add_note}
        if form in forms:
            yield forms[form]()
        else:
            companies = yield self.db.get_companies()
            yield self.render('note.html',
                              companies=companies,
                              form=form)

    @gen.coroutine
    @web.authenticated
    def add_note(self):
        company = self.get_argument('company')
        note_type = self.get_argument('note_type')
        note = self.get_argument('note')
        date = datetime.strptime(self.get_argument('date'), '%m-%d-%Y')
        contact = self.get_argument('contact', None) or None
        try:
            if contact:
                contact = int(contact)
        except ValueError:
            raise web.HTTPError(400, 'contact must be an integer')

        # Store note
        yield self.db.execute(
            "INSERT INTO notes (contact, company, note_type, note_date, note) "
            "VALUES (%s, %s, %s, %s, %s);",
            [contact, company, note_type, date, note])
        yield self.render_form()

    @gen.coroutine
    @web.authenticated
    def view_notes(self):
        yield self.render_form()

    @gen.coroutine
    @web.authenticated
    def render_form(self, companies=None, user=None, **kwargs):
        if self.form is None:
            self.form = self.request.uri[:self.request.uri.find('_')]
        if companies is None:
            companies = yield self.db.get_companies()
        if user is None:
            user = yield self.get_user()
        yield self.render('note.html',
                          companies=companies,
                          user=user,
                          form=self.form,
                          **kwargs)


class GetNotes(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self, company):
        # Get the last 5 notes within the past 90 days
        cursor = yield self.db.execute("SELECT note_date, note_type, first_name, last_name, note "
                                       "FROM notes "
                                       "LEFT OUTER JOIN contact "
                                       "ON (notes.contact = contact.id) "
                                       "WHERE notes.company = %s "
                                       "AND notes.note_date > NOW() - INTERVAL '90 days' "
                                       "ORDER BY note_date DESC "
                                       "LIMIT 5;",
                                       [company])
        notes = cursor.fetchall()
        if len(notes) > 0:
            yield self.render('get_notes.html', notes=notes)
        else:
            self.write('')
