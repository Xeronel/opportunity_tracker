var work_order = {};

work_order.add_consumable = function () {
    var table = $('#consumables').dataTable();
    var part = $('#consumable_part').selectize()[0].selectize.getValue();
    var qty = $('#consume_qty').val();
    var len = $('#consume_amount').val();

    if (!len) {
        return;
    }

    var new_row = {
        part_number: part,
        qty: parseInt(qty) || 1,
        length: len
    };

    table.api().rows().every(function () {
        var row = this.data();
        // If the part and length is the same, add to the qty
        if (row.hasOwnProperty('part_number') &&
            row.part_number === part && row.length === len) {
            new_row.qty += parseInt(row.qty) || 0;
            this.remove();
        }
    });

    if (new_row.part_number) {
        table.api().row.add(new_row);
        table.api().draw();
    }
};

work_order.add_item = function () {
    var table = $('#items').dataTable();
    var part = $('#item_partnumber').selectize()[0].selectize.getValue();
    var qty = parseInt($('#item_qty').val()) || 1;
    var new_row = {
        part_number: part,
        qty: qty,
        length: 0
    };

    api.v1.part.components(part, function (data) {
        // Total the number of kit components to get its length
        // this should be a single item unless the user made an error
        $.each(data, function (idx, e) {
            new_row.length += parseInt(e.qty);
        });

        table.api().rows().every(function () {
            var row = this.data();
            // If the part is the same, add to the qty
            if (row.hasOwnProperty('part_number') && row.part_number === part) {
                new_row.qty += parseInt(row.qty) || 0;
                this.remove();
            }
        });

        if (new_row.part_number) {
            table.api().row.add(new_row);
            table.api().draw();
        }
    });
};

work_order.remove_item = function (e) {
    var table = $(e).dataTable().api();
    var rows = table.rows({selected: true});
    if (rows.count() > 0) {
        rows
            .remove()
            .draw();
    }
};

work_order.submit = function () {
    var table = $('#work-order-form');

    if (table.valid()) {
        var data = {};
        data.consumables = serializeTable('#consumables');
        data.items = serializeTable('#items');
        data.station = $('#station_dropdown').selectize()[0].selectize.getValue();

        $.ajax({
            type: 'POST',
            url: window.location.pathname,
            contentType: 'application/json',
            data: JSON.stringify(data),
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-Xsrftoken', Cookies.get('_xsrf'));
            },
            success: function (data) {
                var alertMessage = $('#alert-message');
                if (alertMessage.length > 0) {
                    alertMessage.remove();
                }
                alert(data);
                table.trigger('reset');
                location.reload();
            },
            error: function () {
                $('#alert').html(
                    '<div id="alert-message" class="alert alert-danger fade in" style="margin-top: -10px">' +
                    '<a class="close" data-dismiss="alert">×</a>' +
                    '<strong>Error!</strong> ' +
                    'Unable to create job! Make sure all field are filled out correctly.' +
                    '</div>'
                );
            }
        });
    }
};

$(function () {
    // Initialize datatables
    var dataTables = [
        {id: '#consumables', title: 'Consumables:'},
        {id: '#items', title: 'Cuts:'}
    ];
    $(dataTables).each(function (idx, e) {
        $(e.id).DataTable({
            sDom: '<"header">frtip',
            bLengthChange: false,
            order: [[1, 'asc']],
            select: {
                style: 'os'
            },
            columnDefs: [
                {
                    targets: 0,
                    orderable: false,
                    className: 'select-checkbox',
                    defaultContent: ''
                }
            ],
            columns: [
                {data: null},
                {data: 'part_number'},
                {data: 'qty'},
                {data: 'length'}
            ]
        });
        $('<label class="pull-left" style="font-weight: 700">' + e.title + '</label>')
            .prependTo(e.id + "_filter");
    });

    // Bind functions to enter key
    var inputs = [
        {id: '#consume_qty', func: work_order.add_consumable},
        {id: '#consume_amount', func: work_order.add_consumable},
        {id: '#item_qty', func: work_order.add_item}
    ];
    $(inputs).each(function (idx, e) {
        $(e.id).keyup(function (event) {
            if (event.keyCode === 13) {
                e.func();
            }
        });
    });

    $('#work-order-form').validate({
        rules: {
            "consumable_part": {
                required: true,
                dataTable: ['#consumables', 'At least 1 consumable is required.']
            },
            "item_partnumber": {
                required: false,
                dataTable: ['#items', 'At least 1 item is required.']
            }
        }
    });
});