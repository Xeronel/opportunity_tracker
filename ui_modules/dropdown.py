from tornado.web import UIModule
from .util import get_path


class NoteTypeDropdown(UIModule):
    def render(self, required=True):
        return self.render_string(get_path('note_type-dropdown.html'),
                                  required=required)


class CompanyDropdown(UIModule):
    def render(self, companies, required=True):
        return self.render_string(get_path('company-dropdown.html'),
                                  companies=companies,
                                  required=required)


class ContactDropdown(UIModule):
    def render(self, required=True):
        return self.render_string(get_path('contact-dropdown.html'),
                                  required=required)


class EmployeeDropdown(UIModule):
    def render(self, employees, required=True):
        return self.render_string(get_path('employee-dropdown.html'),
                                  employees=employees,
                                  required=required)
