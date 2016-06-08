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

// Validator
$.validator.setDefaults({
    highlight: function (element) {
        $(element).closest('.form-group').addClass('has-error');
    },
    unhighlight: function (element) {
        $(element).closest('.form-group').removeClass('has-error');
    },
    errorElement: 'span',
    errorClass: 'help-block',
    errorPlacement: function (error, element) {
        if (element.parent('.input-group').length) {
            error.insertAfter(element.parent());
        } else if (element.closest('.form-group').length > 0) {
            element.closest('.form-group').append(error);
        } else {
            error.insertAfter(element);
        }
    },
    ignore: ':hidden:not([class~=selectized]),:hidden > .selectized, .selectize-control .selectize-input input',
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

// Collapse functions
$('.panel-body.collapse').each(function () {
    $(this)
        .on('hide.bs.collapse', function () {
            $(this).parent().find('.glyphicon-plus').removeClass('glyphicon-plus').addClass('glyphicon-minus');
        })
        .on('show.bs.collapse', function () {
            $(this).parent().find('.glyphicon-minus').removeClass('glyphicon-minus').addClass('glyphicon-plus');
        })
});