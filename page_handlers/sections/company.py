from page_handlers import BaseHandler
from tornado import gen, web
import pycountry
import psycopg2


class Company(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self, form):
        employees = yield self.db.get_employees()
        companies = yield self.db.get_companies()
        yield self.render('company.html',
                          countries=pycountry.countries,
                          employees=employees,
                          companies=companies,
                          form=form)

    @gen.coroutine
    @web.authenticated
    def post(self, form):
        rpc = {'add': self.add_company,
               'mod': self.mod_company,
               'rem': self.rem_company}

        if form in rpc:
            yield rpc[form]()
        else:
            yield self.render_form()

    @gen.coroutine
    @web.authenticated
    def add_company(self):
        employee = self.get_argument('employee')
        company_name = self.get_argument('company-name')
        country = self.get_argument('country')
        address1 = self.get_argument('address1')
        try:
            address2 = self.get_argument('address2')
        except web.MissingArgumentError:
            address2 = ''
        city = self.get_argument('city')
        state = self.get_argument('state')
        postal_code = self.get_argument('zip')
        user_info = yield self.get_user()

        try:
            cursor = yield self.db.execute("INSERT INTO company (name, active, employee, creator) "
                                           "VALUES (%(company_name)s, %(active)s, %(employee)s, %(creator)s) "
                                           "RETURNING id;",
                                           {'company_name': company_name,
                                            'active': True,
                                            'employee': employee,
                                            'creator': user_info.uid})
            company_id = cursor.fetchone()
        except psycopg2.IntegrityError:
            self.send_error(400)
            return

        yield self.db.execute(
            "INSERT INTO location (address1, address2, city, state, country, postal_code, company) "
            "VALUES (%(address1)s, %(address2)s, %(city)s, %(state)s, %(country)s, %(postal_code)s, %(company)s);",
            {'address1': address1,
             'address2': address2,
             'city': city,
             'state': state,
             'country': country,
             'postal_code': postal_code,
             'company': company_id[0]})
        yield self.render_form(user_info)

    @gen.coroutine
    @web.authenticated
    def mod_company(self):
        employee = self.get_argument('employee')
        company = self.get_argument('company')
        company_name = self.get_argument('company-name')
        country = self.get_argument('country')
        address1 = self.get_argument('address1')
        try:
            address2 = self.get_argument('address2')
        except web.MissingArgumentError:
            address2 = ''
        city = self.get_argument('city')
        state = self.get_argument('state')
        postal_code = self.get_argument('zip')

        yield self.db.execute(
            "UPDATE company SET employee = %s, NAME = %s WHERE id = %s;",
            [employee, company_name, company]
        )
        yield self.db.execute(
            "UPDATE location "
            "SET (address1, address2, city, state, postal_code, country) = (%s, %s, %s, %s, %s, %s) "
            "WHERE company = %s;",
            [address1, address2, city, state, postal_code, country, company]
        )
        yield self.render_form()

    @gen.coroutine
    @web.authenticated
    def rem_company(self):
        company_id = self.get_argument('company')
        yield self.db.execute("DELETE FROM company WHERE id = %s;",
                              [company_id])
        yield self.render_form()

    @gen.coroutine
    @web.authenticated
    def render_form(self, user_info=None, form=None, employees=None, companies=None):
        if not form:
            form = self.request.uri.strip('/')[:3]
        if not employees:
            employees = yield self.db.get_employees()
        if not companies:
            companies = yield self.db.get_companies()

        yield self.render('company.html',
                          countries=pycountry.countries,
                          employees=employees,
                          companies=companies,
                          user=user_info,
                          form=form)


class ClearCompany(BaseHandler):
    def get(self):
        self.clear_cookie('company')
