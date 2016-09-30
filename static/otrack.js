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
    $.each(
        $("div[data-date-format]"),
        function (idx, obj) {
            $(obj).datepicker({
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
        }
    );
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
function submit_form(element, message, reload, url) {
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
                    var alertMessage = $('#alert-message');
                    if (alertMessage.length > 0) {
                        alertMessage.remove();
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
                        '<strong>Error!</strong> ' + message +
                        '</div>');
                }
            });
        }
    });
}

// AJAX API
var api = {v1: {}};

// Company
api.v1.company = function (company_id, success) {
    var callback = function (data) {
        data = JSON.parse(data);
        success(data);
    };
    $.get(api.v1.company.url() + company_id, callback);
};
api.v1.company.url = function () {
    return 'api/v1/company/';
};
api.v1.company.url.location = function (company_id) {
    return api.v1.company.url() + company_id + '/location';
};
api.v1.company.url.notes = function (company_id) {
    return api.v1.company.url() + company_id + '/notes';
};
api.v1.company.url.notifications = function (company_id) {
    return api.v1.company.url() + company_id + '/notifications';
};

api.v1.company.location = function (company_id, success) {
    var callback = function (data) {
        data = JSON.parse(data);
        success(data);
    };
    $.get(api.v1.company.url() + company_id + '/location', callback);
};
api.v1.company.notes = function (company_id, success, start_date, end_date) {
    // Check if a start and end date were provided
    // both are required to query a date range but not
    // required to retrieve notes
    start_date = typeof start_date !== 'undefined' ? start_date : false;
    end_date = typeof end_date !== 'undefined' ? end_date : false;
    var data = {
        start_date: start_date,
        end_date: end_date
    };
    var callback = function (data) {
        data = JSON.parse(data);
        success(data);
    };

    if (start_date !== false && end_date !== false) {
        $.get(api.v1.company.url() + company_id + '/notes', data, callback);
    } else {
        $.get(api.v1.company.url() + company_id + '/notes', callback);
    }
};
api.v1.company.notifications = function (company_id, success, start_date, end_date) {
    start_date = typeof start_date !== 'undefined' ? start_date : false;
    end_date = typeof end_date !== 'undefined' ? end_date : false;
    var data = {
        start_date: start_date,
        end_date: end_date
    };
    var callback = function (data) {
        data = JSON.parse(data);
        success(data);
    };

    if (start_date !== false && end_date !== false) {
        $.get(api.v1.company.url() + company_id + '/notifications', data, callback)
    } else {
        $.get(api.v1.company.url() + company_id + '/notifications', callback)
    }
};
api.v1.company.employee = function (company_id, success) {
    var callback = function (data) {
        data = JSON.parse(data);
        success(data);
    };
    $.get(api.v1.company.url() + company_id + '/employee', callback);
};

// Employee
api.v1.employee = {};
api.v1.employee.url = function () {
    return 'api/v1/employee/';
};
api.v1.employee.url.notifications = function (employee_id) {
    return api.v1.employee.url() + employee_id + '/notifications';
};
api.v1.employee.url.companies = function (employee_id) {
    return api.v1.employee.url() + employee_id + '/companies';
};

api.v1.employee.notifications = function (employee_id, success, start_date, end_date) {
    start_date = typeof start_date !== 'undefined' ? start_date : false;
    end_date = typeof end_date !== 'undefined' ? end_date : false;
    var data = {
        start_date: start_date,
        end_date: end_date
    };
    var callback = function (data) {
        data = JSON.parse(data);
        success(data);
    };

    if (start_date !== false && end_date !== false) {
        $.get(api.v1.employee.url() + employee_id + '/notifications', data, callback);
    } else {
        $.get(api.v1.employee.url() + employee_id + '/notifications', callback);
    }
};
api.v1.employee.companies = function (employee_id, success) {
    var callback = function (data) {
        data = JSON.parse(data);
        success(data);
    };
    $.get(api.v1.employee.url() + employee_id + '/companies', callback);
};