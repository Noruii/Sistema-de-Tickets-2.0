// Funciones para mostrar la contraseña

// TODO: Arreglar repeticion...

function password_show_hide_pass1(event) {
    event.preventDefault()

    var id_password1 = document.getElementById("id_password1");
    var show_eye_pass1 = document.getElementById("show_eye_pass1");
    var hide_eye_pass1 = document.getElementById("hide_eye_pass1");

    if (id_password1.type === "password") {
        id_password1.type = "text";
        hide_eye_pass1.classList.remove("d-none");
        show_eye_pass1.classList.add("d-none");

    } else {
        id_password1.type = "password";
        hide_eye_pass1.classList.add("d-none");
        show_eye_pass1.classList.remove("d-none");

    }
}

function password_show_hide_pass2(event) {
    event.preventDefault()

    var id_password2 = document.getElementById("id_password2");
    var show_eye_pass2 = document.getElementById("show_eye_pass2");
    var hide_eye_pass2 = document.getElementById("hide_eye_pass2");

    if (id_password2.type === "password") {
        id_password2.type = "text";
        hide_eye_pass2.classList.remove("d-none");
        show_eye_pass2.classList.add("d-none");

    } else {
        id_password2.type = "password";
        hide_eye_pass2.classList.add("d-none");
        show_eye_pass2.classList.remove("d-none");

    }
}

function password_show_hide_modal(event) {
    event.preventDefault()

    var id_passwordModal = document.getElementById("id_passwordModal");
    var show_eye_modal = document.getElementById("show_eye_modal");
    var hide_eye_modal = document.getElementById("hide_eye_modal");

    if (id_passwordModal.type === "password") {
        id_passwordModal.type = "text";
        hide_eye_modal.classList.remove("d-none");
        show_eye_modal.classList.add("d-none");

    } else {
        id_passwordModal.type = "password";
        hide_eye_modal.classList.add("d-none");
        show_eye_modal.classList.remove("d-none");

    }
}
