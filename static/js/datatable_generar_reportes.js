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
            layout: 'columns-5'
        },
        dom: 'PBfrtip', //PB para poder utilizar botones y searchpanels al mismo tiempo
        columnDefs: [
            {
                searchPanes: {
                    show: true
                },
                targets: [1, 2, 3, 5, 6]
            }
        ],
    
        // autowidth: false,
        "language": {
            url : "//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json"
        },
        // buttons: [
        //     {
        //         extend: 'excelHtml5',
        //         text: '<i class="fa-solid fa-file-excel"></i> ',
        //         titleAttr: 'Exportar a Excel',
        //         className: 'btn btn-outline-success',
        //     },
        //     {
        //         extend: 'pdfHtml5',
        //         text: '<i class="fa-solid fa-file-pdf"></i> ',
        //         titleAttr: 'Exportar a PDF',
        //         className: 'btn btn-outline-danger',
        //         download: 'open',
        //         //orientation: 'landscape',
        //         pageSize: 'LEGAL',
        //     },
        //     {
        //         extend: 'print',
        //         text: '<i class="fa-solid fa-print"></i>',
        //         titleAttr: 'Imprimir',
        //         className: 'btn btn-outline-info',
        //     },
        // ]
    });
});