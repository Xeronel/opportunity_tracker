from tornado.web import UIModule
import settings
import os


_ui_path = os.path.join(settings.TEMPLATE_PATH, 'ui')


def _get_path(file_name):
    return os.path.join(_ui_path, file_name)


class ActionTakenDropdown(UIModule):
    def render(self):
        return self.render_string(_get_path('actiontaken-dropdown.html'))


class CompanyDropdown(UIModule):
    def render(self, companies):
        return self.render_string(_get_path('company-dropdown.html'), companies=companies)


class ContactDropdown(UIModule):
    def render(self):
        return self.render_string(_get_path('contact-dropdown.html'))
