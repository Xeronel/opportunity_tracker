from tornado.web import UIModule
from .util import get_path


class DatePicker(UIModule):
    def render(self, name="date", label='Select Date',
               classes="col-lg-3 col-md-3", required=True, readonly=True):
        return self.render_string(get_path('datepicker.html'),
                                  classes=classes,
                                  required=required,
                                  readonly=readonly,
                                  label=label,
                                  name=name)
