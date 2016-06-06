from tornado.web import UIModule
from config import Config
import os


config = Config()


def _get_path(file_name):
    return os.path.join('ui', file_name)


class ActionTakenDropdown(UIModule):
    def render(self):
        return self.render_string(_get_path('actiontaken-dropdown.html'))


class CompanyDropdown(UIModule):
    def render(self, companies):
        return self.render_string(_get_path('company-dropdown.html'), companies=companies)


class ContactDropdown(UIModule):
    def render(self):
        return self.render_string(_get_path('contact-dropdown.html'))


class EmployeeDropdown(UIModule):
    def render(self, employees):
        return self.render_string(_get_path('employee-dropdown.html'), employees=employees)
