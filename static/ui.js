function loadContacts(company) {
    var contacts = $('#contact');
    if (contacts.length > 0) {
        var contact_selectize = contacts[0].selectize;
        contact_selectize.clearOptions();
        contact_selectize.addOption({'text': 'None', 'value': 'None'});
        $.getJSON({
            url: '/get_contacts/' + company,
            success: function (data) {
                if (data != '') {
                    contact_selectize.addOption(data);
                }
            }
        });
    }
}

function initDatePicker(id, date) {
    $(id).datepicker({
        autoclose: true,
        todayHighlight: true
    })
        .datepicker('update', date)
        .on('changeDate', function (e) {
            var control = $(e.target).closest('.form-group');
            if (control.hasClass('has-error')) {
                control.removeClass('has-error');
                $(control).children('span.help-block').remove();
            }
        });
}

$(function () {
    var options = {
        selectOnTab: true,
        onChange: function (value) {
            var control = $(this.$dropdown).closest('.form-group');
            if (control.hasClass('has-error')) {
                control.removeClass('has-error');
                $(control).children('span.help-block').remove();
            }
        }
    };

    // id, default value
    var dropdowns = [
        {id: '#note_type', value: ''},
        {id: '#contact', value: ''},
        {id: '#country', value: 'US'},
        {id: '#employee', value: ''}
    ];
    for (var i = 0; i < dropdowns.length; i++) {
        var e = $(dropdowns[i].id);
        if (e.length > 0) {
            if (dropdowns[i].value) {
                e.selectize(options)[0].selectize.setValue(dropdowns[i].value);
            } else {
                e.selectize(options);
            }
        }
    }

    // Contact dropdown
    var contact = $('#contact');
    if (contact.length > 0) {
        contact = contact.selectize()[0].selectize;
        contact.on('change', function (value) {
            if (value === 'None') {
                contact.clear();
            }
        })
    }

    // Company dropdown
    var company = $('#company');
    if (company.length > 0) {
        company = company.selectize({
            onChange: function (value) {
                Cookies.set('company', value);
                var control = $(this.$dropdown).closest('.form-group');
                if (control.hasClass('has-error')) {
                    control.removeClass('has-error');
                    $(control).children('span.help-block').remove();
                }
            },
            selectOnTab: true
        });

        company = company[0].selectize;
        company.on('change', function (value) {
            $(function () {
                loadContacts(value);
            });
        });

        company.on('reset', function (value) {
            $(function () {
                loadContacts(value);
            })
        });

        var cookie = Cookies.get('company');
        if (cookie) {
            company.setValue(cookie);
        }
    }
});