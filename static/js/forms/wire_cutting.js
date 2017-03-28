var wire_cutting = {};

wire_cutting.add_reel = function () {
    var table = $('#reels').dataTable();
    var part = $('#reel_partnumber').selectize()[0].selectize.getValue();
    var qty = $('#reel_qty').val();
    var len = $('#reel_len').val();

    var new_row = {
        part_number: part,
        qty: parseInt(qty),
        length: len
    };

    table.api().rows().every(function () {
        var row = this.data();
        // If the part and length is the same, add to the qty
        if (row.hasOwnProperty('part_number') &&
            row.part_number === part && row.length === len) {
            new_row.qty += parseInt(row.qty);
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
    var qty = parseInt($('#cut_qty').val());
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
                new_row.qty += parseInt(row.qty);
                this.remove();
            }
        });

        if (new_row.part_number) {
            table.api().row.add(new_row);
            table.api().draw();
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
});