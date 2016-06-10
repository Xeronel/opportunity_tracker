from tornado.web import UIModule
import os


def _get_path(file_name):
    return os.path.join('ui', file_name)


class ActionTakenDropdown(UIModule):
    def render(self, required=True):
        return self.render_string(_get_path('actiontaken-dropdown.html'),
                                  required=required)


class CompanyDropdown(UIModule):
    def render(self, companies, required=True):
        return self.render_string(_get_path('company-dropdown.html'),
                                  companies=companies,
                                  required=required)


class ContactDropdown(UIModule):
    def render(self, required=True):
        return self.render_string(_get_path('contact-dropdown.html'),
                                  required=required)


class EmployeeDropdown(UIModule):
    def render(self, employees, required=True):
        return self.render_string(_get_path('employee-dropdown.html'),
                                  employees=employees,
                                  required=required)
