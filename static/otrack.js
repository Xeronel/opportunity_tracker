// Dropdown
$(".dropdown-menu li a").click(function(){
    var selText = $(this).text();
    $(this).parents('.dropdown').find('.dropdown-toggle').html(selText + ' <span class="caret"></span>');
    var inputField = $(this).parents('.dropdown').find('input');
    if (inputField.length == 1) {
        inputField[0].value = selText;
    }
});

// Date picker
$(function() {
    $("#datepicker").datepicker({
        autoclose: true,
        todayHighlight: true
    }).datepicker('update', new Date());
});

// Nav selector
function navSelector(id) {
    $(".nav ul li").removeClass("active");
    $('#'+id).addClass('active');
}

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