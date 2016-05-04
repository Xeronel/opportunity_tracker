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