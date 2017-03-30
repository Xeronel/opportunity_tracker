from tornado.web import UIModule
from .util import get_path


class NoteTypeDropdown(UIModule):
    def render(self, required=True):
        return self.render_string(get_path('note_type-dropdown.html'),
                                  required=required)


class CompanyDropdown(UIModule):
    def render(self, companies,
               classes='form-group col-md-6 col-lg-5',
               required=True):
        return self.render_string(get_path('company-dropdown.html'),
                                  classes=classes,
                                  companies=companies,
                                  required=required)


class ContactDropdown(UIModule):
    def render(self, required=True):
        return self.render_string(get_path('contact-dropdown.html'),
                                  required=required)


class EmployeeDropdown(UIModule):
    def render(self, employees, label="Employee:",
               classes="", required=True):
        return self.render_string(get_path('employee-dropdown.html'),
                                  employees=employees,
                                  classes=classes,
                                  label=label,
                                  required=required)


class UOMDropdown(UIModule):
    def render(self, uoms, required=True, label="Unit of Measure:", classes="form-group"):
        return self.render_string(get_path('uom-dropdown.html'),
                                  uoms=uoms,
                                  classes=classes,
                                  label=label,
                                  required=required)


class PartTypeDropdown(UIModule):
    def render(self, part_types, required=True, label="Type:", classes="form-group"):
        return self.render_string(get_path('part_type-dropdown.html'),
                                  part_types=part_types,
                                  classes=classes,
                                  label=label,
                                  required=required)


class PartNumberDropdown(UIModule):
    def render(self, part_numbers, required=True, label="Part Number:", classes="form-group",
               uid="part_number_dropdown", name="part_number"):
        return self.render_string(get_path('part_number-dropdown.html'),
                                  part_numbers=part_numbers,
                                  uid=uid,
                                  name=name,
                                  label=label,
                                  classes=classes,
                                  required=required)


class WireStationDropdown(UIModule):
    def render(self, wire_stations, required=True, label="Wire Station:", classes="form-group",
               uid="wire_station_dropdown", name="wire_station"):
        return self.render_string(get_path('wire_station-dropdown.html'),
                                  wire_stations=wire_stations,
                                  uid=uid,
                                  name=name,
                                  label=label,
                                  classes=classes,
                                  required=required)
