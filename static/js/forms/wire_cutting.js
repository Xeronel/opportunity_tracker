$(function () {
    $('#reels').DataTable({
        sDom: '<"header">frtip',
        bLengthChange: false,
        select: {
            style: 'os'
        }
    });
});