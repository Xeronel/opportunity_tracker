var wire_cutting = {};

wire_cutting.add_part = function (tbl_id, part_id, qty_id, len_id) {
    var table = $(tbl_id).dataTable();
    var part = $(part_id).selectize()[0].selectize.getValue();
    var qty = $(qty_id).val();
    var len = $(len_id).val();

    var new_row = {
        part_number: part,
        qty: parseInt(qty),
        length: len
    };

    table.api().rows().every(function () {
        var row = this.data();
        // If the part and length is the same, add to the qty
        if (row.hasOwnProperty('part_number') &&
            row.part_number == part && row.length == len) {
            new_row.qty +=  parseInt(row.qty);
            this.remove();
        }
    });

    if (new_row.part_number) {
        table.api().row.add(new_row);
        table.api().draw();
    }
};

$(function () {
    var dataTables = [
        {id: '#reels', title: 'Reels:'},
        {id: '#cuts', title:'Cuts:'}
    ];

    // Initialize datatables
    $(dataTables).each(function(idx, e) {
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