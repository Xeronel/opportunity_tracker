var wire_cutting = {};

wire_cutting.add_reel = function () {
    var table = $('#reels').dataTable();
    var part = $('#reel_partnumber').selectize()[0].selectize.getValue();
    var qty = $('#reel_qty').val();
    var len = $('#reel_len').val();

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

wire_cutting.add_cut = function () {
    var table = $('#cuts').dataTable();
    var part = $('#cut_partnumber').selectize()[0].selectize.getValue();
    var qty = parseInt($('#cut_qty').val()) || 1;
    var new_row = {
        part_number: part,
        qty: qty,
        length: 0
    };

    api.v1.part.components(part, function (data) {
        // Total the number of kit components to get its length
        // this should be a single wire unless the user made an error
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

wire_cutting.remove_item = function (e) {
    var table = $(e).dataTable().api();
    var rows = table.rows({selected: true});
    if (rows.count() > 0) {
        rows
            .remove()
            .draw();
    }
};

wire_cutting.submit = function () {
    var table = $('#wire-cutting-form');
    var data = {};
    data.reels = serializeTable('#reels');
    data.cuts = serializeTable('#cuts');
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
};

$(function () {
    var dataTables = [
        {id: '#reels', title: 'Reels:'},
        {id: '#cuts', title: 'Cuts:'}
    ];

    // Initialize datatables
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

    var inputs = [
        {id: '#reel_qty', func: wire_cutting.add_reel},
        {id: '#reel_len', func: wire_cutting.add_reel},
        {id: '#cut_qty', func: wire_cutting.add_cut}
    ];

    // Bind functions to enter key
    $(inputs).each(function (idx, e) {
        $(e.id).keyup(function (event) {
            if (event.keyCode === 13) {
                e.func();
            }
        });
    });
});