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
    'alignright,alignjustify,bullist,numlist,outdent,indent',
    setup: function (ed) {
        ed.on('change', function () {
            tinymce.triggerSave();
            $("#" + ed.id).valid();
        })
    }
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
    ignore: [
        ':hidden:not([class~=selectized]),:hidden > .selectized, .selectize-control .selectize-input input',
        ':hidden:not(textarea)']
});

// Date picker
$(function () {
    $("#datepicker").datepicker({
        autoclose: true,
        todayHighlight: true
    })
        .datepicker('update', new Date())
        .on('changeDate', function (e) {
            var control = $(e.target).closest('.form-group');
            if (control.hasClass('has-error')) {
                control.removeClass('has-error');
                $(control).children('span.help-block').remove();
            }
        });
});

// Nav selector
function navSelector(id) {
    $(".nav .panel div").removeClass("active");
    $('#' + id)
        .addClass('active')
        .parent('div').addClass('in');
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

// AJAX Submit a form
function submit_form(element, url, reload) {
    url = typeof url !== 'undefined' ? url : window.location.pathname;
    reload = typeof reload !== 'undefined' ? reload : false;
    element.submit(function (event) {
        event.preventDefault();
        if ($(this).valid()) {
            $.ajax({
                type: 'POST',
                url: url,
                data: element.serialize(),
                success: function () {
                    if ($('#alert-message').length > 0) {
                        $('#alert-message').remove();
                    }
                    element.trigger('reset');
                    if (reload === true) {
                        location.reload();
                    }
                },
                error: function () {
                    $('#alert').html(
                        '<div id="alert-message" class="alert alert-danger fade in" style="margin-top: -10px">' +
                        '<a class="close" data-dismiss="alert">×</a>' +
                        '<strong>Error!</strong> A company with that name already exists!' +
                        '</div>');
                }
            });
        }
    });
}