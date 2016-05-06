function loadContacts(company) {
    var contacts = $('#contact');
    if (contacts.length > 0) {
        var contact_selectize = contacts[0].selectize;
        contact_selectize.clearOptions();
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

$(function () {
    // Action Taken dropdown
    var action_taken = $('#action');
    if (action_taken.length > 0) {
        action_taken.selectize();
    }

    // Contact dropdown
    var contact = $('#contact');
    if (contact.length > 0) {
        contact.selectize();
    }

    // Company dropdown
    var company = $('#company');
    if (company.length > 0) {
        company = company.selectize({
            onChange: function (value) {
                Cookies.set('company', value);
            }
        });

        company = company[0].selectize;
        company.on('change', function (value) {
            $(function () {
                loadContacts(value);
            });
        });

        var cookie = Cookies.get('company');
        if (cookie) {
            company.setValue(cookie);
        }
    }
});