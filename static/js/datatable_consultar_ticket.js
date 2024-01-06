$(function () {
    $('#data').DataTable({
        responsive: true,
        responsive: {
            details: {
                display: DataTable.Responsive.display.modal({
                    header: function (row) {
                        var data = row.data();
                        return 'Detalles para ' + data[1] +": "+ data[2];
                    }
                }),
                renderer: DataTable.Responsive.renderer.tableAll({
                    tableClass: 'table'
                })
            }
        },

        searchPanes: {
            initCollapsed: true,
            cascadePanes: true,
            layout: 'columns-6',
            columns: [1, 2, 3, 5, 6, 7]
        },
        dom: 'Plfrtip', // https://datatables.net/reference/option/dom
        columnDefs: [
            {
                searchPanes: {
                    show: true
                },
                targets: [1, 2, 3, 5, 6, 7]
            }
        ],

        // autowidth: false,
        "language": {
            url : "//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json"
        },
    });
});