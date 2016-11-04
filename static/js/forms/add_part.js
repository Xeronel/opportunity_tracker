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
            selector: 'td:first-child'
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
        select: {
            style: 'os',
            selector: 'td:first-child'
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

    $('#add_part_form').validate({
        rules: {
            cost: {
                required: true,
                money: true
            }
        }
    });

    $()
});