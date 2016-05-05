// Editor
tinymce.init({
    selector: 'textarea',
    menubar: false,
    skin: 'light',
    skin_url: '/static/light',
    forced_root_block: false,
    theme_advanced_resizing: true,
    theme_advanced_resize_horizontal: false,
    theme_advanced_statusbar_location: 'bottom',
    toolbar: 'undo,redo,bold,italic,alignleft,aligncenter,' +
    'alignright,alignjustify,bullist,numlist,outdent,indent'
});

// Dropdown
$(".dropdown-menu li a").click(function () {
    var selText = $(this).text();
    $(this).parents('.dropdown').find('.dropdown-toggle').html(selText + ' <span class="caret"></span>');
    var inputField = $(this).parents('.dropdown').find('input');
    if (inputField.length == 1) {
        inputField[0].value = selText;
    }
});

// Date picker
$(function () {
    $("#datepicker").datepicker({
        autoclose: true,
        todayHighlight: true
    }).datepicker('update', new Date());
});

// Nav selector
function navSelector(id) {
    $(".nav ul li").removeClass("active");
    $('#' + id).addClass('active');
}