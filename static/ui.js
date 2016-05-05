$(function () {
    // Company Dropdown
    var company = $('#company');
    if (company.length > 0) {
        company = company.selectize({
            onChange: function (value) {
                Cookies.set('company', value);
            }
        });

        company = company[0].selectize;
        var cookie = Cookies.get('company');
        if (cookie) {
            company.setValue(cookie);
        }
    }

    // Action Taken Dropdown
    var action_taken = $('#action');
    if (action_taken.length > 0) {
        action_taken = action_taken.selectize();
    }
});