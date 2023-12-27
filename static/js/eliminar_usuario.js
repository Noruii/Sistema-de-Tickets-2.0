function eliminar_usuario(id) {
    Swal.fire({
        title: "¿Está seguro?",
        text: "Esta acción no se puede deshacer.",
        icon: "warning",
        showCancelButton: true,
        cancelButtonText: '<i class="fa-solid fa-xmark"></i> No, Cancelar',
        confirmButtonText: '<i class="fa-solid fa-trash"></i> Si, Eliminar',
        confirmButtonColor: "#dc3545",
        customClass: {
            confirmButton: 'btn btn-danger mr-2',
            cancelButton: 'btn btn-secondary'
        },
        buttonsStyling: false,
        showLoaderOnConfirm: true,
        preConfirm: () => {
            return new Promise((resolve, reject) => {
                // Abrir un nuevo SweetAlert para pedir la contraseña
                Swal.fire({
                    title: 'Confirmar con su contraseña',
                    input: 'password',
                    inputAttributes: {
                        autocapitalize: 'off'
                    },
                    showCancelButton: true,
                    cancelButtonText: '<i class="fa-solid fa-xmark"></i> Cancelar',
                    confirmButtonText: '<i class="fa-solid fa-trash"></i> Confirmar',
                    confirmButtonColor: "#dc3545",
                    customClass: {
                        confirmButton: 'btn btn-danger mr-2',
                        cancelButton: 'btn btn-secondary'
                    },
                    showLoaderOnConfirm: true,
                    preConfirm: (password) => {
                        console.log('La contraseña ingresada es: ', password);
                        return fetch('/sdt/validar_contrasena/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCookie('csrftoken') // Obtener el token CSRF
                            },
                            // Enviando la contraseña como JSON
                            body: JSON.stringify({ password: password })
                        })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error(response.statusText)
                            }
                            return response.json()
                        })
                        .then(data => {
                            console.log('data: ', data)
                            if (data.valid) {
                                // Si la contraseña es válida, proceder con la eliminación
                                window.location.href = "/sdt/eliminar_usuario/" + id + "/";
                            } else {
                                // Mostrar mensaje de contraseña incorrecta
                                Swal.showValidationMessage(`Contraseña incorrecta. Vuelva a intentarlo.`)
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error)
                        })
                    },
                    allowOutsideClick: () => !Swal.isLoading()
                })
            })
        }
    });

    // Función para obtener el token CSRF de las cookies
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
}