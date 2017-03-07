var add_part = {};

add_part.toggleKit = function (part_type) {
    if (part_type.getValue() === 'KIT') {
        $('.kit-row').removeClass('hidden');
    } else {
        $('.kit-row').addClass('hidden');
    }
};

add_part.inputQty = function (target) {
    var element = $(target);
    var part_list = $('#part-list').dataTable().api();
    var row = part_list.row(element.parent());
    var row_data = row.data();

    if (element.is('input')) {
        if (/^\d+$/.test(element.val())) {
            row_data['qty'] = parseInt(element.val());
            row.data(row_data);
            element.remove();
        }
    }
};

add_part.addItem = function () {
    var part_list = $('#part-list').dataTable().api();
    var bill_of_materials = $('#bill-of-materials').dataTable();
    var rows = part_list.rows({selected: true}).data();

    $.each(rows, function (index, row) {
        var found = bill_of_materials.fnFindCellRowIndexes(row, 0);
        if (found.length === 0) {
            if (row.hasOwnProperty('qty') && row['qty'] > 0) {
                bill_of_materials.api().row.add(row)
            } else {
                alert('Skipping ' + row['part_number'] + ' (qty must be greater than 0)');
            }
        } else {
            alert(row['part_number'] + ' is already in the bill of materials!');
        }
    });
    bill_of_materials.api().draw();
};

add_part.removeItem = function () {
    var bill_of_materials = $('#bill-of-materials').dataTable().api();
    var row = bill_of_materials.rows({selected: true});

    if (row.count() > 0) {
        row
            .remove()
            .draw();
    }
};

add_part.serializeTable = function (element) {
    var data = $(element).dataTable().api().data();
    var result = [];

    for (var i = 0; i < data.length; i++) {
        result.push(data[i]);
    }
    return result;
};

add_part.serializeForm = function (element) {
    var data = $(element).serializeArray();
    var result = {};

    for (var i = 0; i < data.length; i++) {
        if (data[i].hasOwnProperty('name') && data[i].hasOwnProperty('value')) {
            result[data[i].name] = data[i].value;
        } else {
            console.log(data[i] + ' missing name or value');
        }
    }
    return result;
};

add_part.submit = function () {
    var element = $("#add-part-form");
    if (element.valid()) {
        var data = add_part.serializeForm('#add-part-form');
        data.bill_of_materials = add_part.serializeTable('#bill-of-materials');

        if (data.part_type.toString() === 'KIT' && data.bill_of_materials.length < 0) {
            $('#alert').html();
            return
        }

        $.ajax({
            type: 'POST',
            url: window.location.pathname,
            contentType: 'application/json',
            data: JSON.stringify(data),
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-Xsrftoken', Cookies.get('_xsrf'));
            },
            success: function () {
                var alertMessage = $('#alert-message');
                if (alertMessage.length > 0) {
                    alertMessage.remove();
                }
                element.trigger('reset');
                location.reload();
            },
            error: function () {
                $('#alert').html(
                    '<div id="alert-message" class="alert alert-danger fade in" style="margin-top: -10px">' +
                    '<a class="close" data-dismiss="alert">×</a>' +
                    '<strong>Error!</strong> ' +
                    'Unable to submit part! Make sure all field are filled out correctly.' +
                    '</div>');
            }
        });
    }
};

$(function () {
    var part_type = $('#part_type').selectize()[0].selectize;
    part_type.on('change', function () {
        add_part.toggleKit(part_type)
    });
    add_part.toggleKit(part_type);

    var part_list = $('#part-list').DataTable({
        sDom: '<"header">frtip',
        bLengthChange: false,
        order: [[1, 'asc']],
        select: {
            style: 'os',
            selector: 'td:nth-child(-n+6)'
        },
        ajax: {
            url: api.v1.part.url.parts(),
            dataSrc: '',
            type: 'GET'
        },
        columnDefs: [
            {
                targets: 0,
                orderable: false,
                className: 'select-checkbox',
                defaultContent: ''
            },
            {
                targets: 6,
                data: 'qty',
                render: function (data, type, row) {
                    if (row.hasOwnProperty('qty')) {
                        return row['qty'];
                    } else {
                        return 0;
                    }
                }
            }
        ],
        columns: [
            {data: null},
            {data: "part_number"},
            {data: "description"},
            {data: "uom"},
            {data: "cost"},
            {data: "part_type"},
            {data: null}
        ]
    });
    $('<label class="pull-left" style="font-weight: 700">Part List:</label>').prependTo("#part-list_filter");

    $('#bill-of-materials').DataTable({
        sDom: '<"header">frtip',
        bLengthChange: false,
        order: [[1, 'asc']],
        select: {
            style: 'os',
            selector: 'td:nth-child(-n+6)'
        },
        columnDefs: [{
            targets: 0,
            orderable: false,
            className: 'select-checkbox',
            defaultContent: ''
        }],
        columns: [
            {data: null},
            {data: 'part_number'},
            {data: 'description'},
            {data: 'uom'},
            {data: 'cost'},
            {data: 'part_type'},
            {data: 'qty'}
        ]
    });
    $('<label class="pull-left" style="font-weight: 700">Bill Of Materials:</label>')
        .prependTo("#bill-of-materials_filter");

    part_list.on('click', 'tbody td:nth-child(7)', function () {
        var element = $(this);
        var children = element.children();
        var row = part_list.row(this);
        if (children.length === 0 || !$(children.get(0)).is('input')) {
            var row_id = '"qty-' + row.index() + '"';
            var row_qty = element.text();
            element.html(
                '<input id=' + row_id + ' class="form-control" type="text" ' +
                'value="' + row_qty + '" onblur="add_part.inputQty(this)">'
            );
            var input = element.find('input');
            input.focus();
            input.select();
            input.on('keyup keypress', function (e) {
                var keyCode = e.keyCode || e.which;
                if (keyCode == 13) {
                    e.preventDefault();
                    add_part.inputQty(e.target);
                }
            });
        }
    });

    jQuery.validator.addMethod('kitBOM', function (value, element) {
        var result = false;
        var bom_rows = $('#bill-of-materials > tbody tr');
        var is_kit = $('#part_type').selectize()[0].selectize.getValue() === 'KIT';

        if (!is_kit) {
            result = true;
        } else if (bom_rows.length === 1 && bom_rows[0].innerText !== 'No data available in table') {
            result = true;
        } else if (bom_rows.length > 1) {
            result = true;
        }

        return this.optional(element) || result;
    }, "Bill of materials can't be empty.");

    $('#add-part-form').validate({
        rules: {
            "cost": {
                required: true,
                money: true
            },
            "part_type": {
                required: true,
                kitBOM: true
            }
        }
    });
});