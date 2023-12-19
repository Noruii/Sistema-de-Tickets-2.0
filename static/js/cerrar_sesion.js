function cerrar_sesion() {
    Swal.fire({
        title: "¿Está seguro de que quiere cerrar sesión?",
        // text: "Esta ación no se puede deshacer.",
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
            window.location.href = "/sdt/cerrar_sesion/";
        }
        //else if (result.isDismissed) {
        //    Swal.fire('Changes are not saved', '', 'info')
        //}
    });
}