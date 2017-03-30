from page_handlers import BaseHandler
from tornado import gen, web


class Project(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self, form):
        if form == 'manage':
            cursor = yield self.db.execute(
                "SELECT DISTINCT company.id, company.name "
                "FROM project "
                "LEFT JOIN company ON company = company.id;"
            )
            companies = cursor.fetchall()
        else:
            companies = yield self.db.get_companies()
        yield self.render('project.html',
                          companies=companies,
                          form=form)

    @gen.coroutine
    @web.authenticated
    def post(self, form):
        forms = {'add': self.add_project}
        companies = yield self.db.get_companies()
        if form in forms:
            yield forms[form]()

        yield self.render('project.html',
                          companies=companies,
                          form=form)

    @gen.coroutine
    def add_project(self):
        project_name = self.get_argument('project')
        project_path = self.get_argument('path')
        company_id = self.get_argument('company')
        description = self.get_argument('description')
        yield self.db.execute(
            """
            INSERT INTO project (name, description, company, path)
            VALUES (%s, %s, %s, %s);
            """,
            [project_name.lower(), description, company_id, project_path.lower()]
        )


class ProjectRouter(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self, company, project, form=None):
        try:
            yield self.render('projects/%s/%s/%s.html' % (company, project, project),
                              form=form)
        except FileNotFoundError:
            self.send_error(404)
