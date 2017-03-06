$(function () {
    // Reels DataTable
    $('#reels').DataTable({
        sDom: '<"header">frtip',
        bLengthChange: false,
        select: {
            style: 'os'
        }
    });
    $('<label class="pull-left" style="font-weight: 700">Reels:</label>')
        .prependTo("#reels_filter");

    // Cuts DataTable
    $('#cuts').DataTable({
        sDom: '<"header">frtip',
        bLengthChange: false,
        select: {
            style: 'os'
        }
    });
    $('<label class="pull-left" style="font-weight: 700">Cuts:</label>')
        .prependTo("#cuts_filter");
});