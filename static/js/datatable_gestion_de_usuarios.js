$(function () {
    $('#data').DataTable({
        responsive: true,
        responsive: {
            details: {
                display: DataTable.Responsive.display.modal({
                    header: function (row) {
                        var data = row.data();
                        return 'Detalles para ' + data[1] +": "+ data[2]+" "+ data[3];
                    }
                }),
                renderer: DataTable.Responsive.renderer.tableAll({
                    tableClass: 'table'
                })
            }
        },
        pageLength : 8,
        lengthMenu: [[8, 10, 20, -1], [8, 10, 20, 'Todos']],
        // autowidth: false,
        "language": {
            url : "//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json"
        },
    });
});
