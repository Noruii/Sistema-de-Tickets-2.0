function cambiar_estado_prioridad(id) {
    Swal.fire({
        title: "¿Está seguro?",
        text: "Esta acción cambiará el estado y prioridad del ticket.",
        icon: "warning",
        showCancelButton: true,
        cancelButtonText: '<i class="fa-solid fa-xmark"></i> No &nbsp;',
        confirmButtonText: '<i class="fa-solid fa-right-from-bracket"></i> Si &nbsp;',
        confirmButtonColor: "#dc3545",
        customClass: {
            confirmButton: 'btn btn-danger mr-2',
            cancelButton: 'btn btn-secondary'
        },
        buttonsStyling: false,
        showLoaderOnConfirm: true,
        preConfirm: () => {
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    resolve()
                }, 800)
            })
        }
    })
    .then(function (result) {
        if (result.isConfirmed) {
            document.getElementById(`cambiarEstadoForm_${id}`).submit()
        }
        else if (result.isDismissed) {
            Swal.fire('No se guardaron los cambios.', '', 'info')
        }
    });
}