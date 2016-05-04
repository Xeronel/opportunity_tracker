$(function () {
    if ($('#company').length > 0) {
        var $company = $('#company').selectize();
        var company = $company[0].selectize;

        var cookie = Cookies.get('company');
        if (cookie) {
            company.setValue(cookie);
        }
    }
});

$(".form-control#company").change(function () {
    Cookies.set('company', $(this).find('option:selected').val());
});