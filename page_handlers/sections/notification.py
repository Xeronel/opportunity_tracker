from page_handlers import BaseHandler
from tornado import gen, web
from datetime import datetime


class Notification(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self, form):
        companies = yield self.db.get_companies()
        employees = yield self.db.get_employees()
        yield self.render('notification.html',
                          companies=companies,
                          employees=employees,
                          form=form)

    @gen.coroutine
    @web.authenticated
    def post(self, form):
        companies = yield self.db.get_companies()
        company = self.get_argument('company')
        notify_date = datetime.strptime(self.get_argument('date'), '%m-%d-%Y')
        note = self.get_argument('note')
        uid = self.get_secure_cookie('uid').decode('utf-8')
        yield self.db.execute("INSERT INTO notification (company, notify_date, note, employee) "
                              "VALUES (%s, %s, %s, %s)",
                              [company, notify_date.strftime('%Y-%m-%d'), note, uid])
        yield self.render('notification.html', companies=companies)
