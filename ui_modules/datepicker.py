from tornado.web import UIModule
from .util import get_path


class DatePicker(UIModule):
    def render(self, name="date", label='Select Date', required=True, readonly=True):
        return self.render_string(get_path('datepicker.html'),
                                  required=required,
                                  readonly=readonly,
                                  label=label,
                                  name=name)
