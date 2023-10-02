document.addEventListener('DOMContentLoaded', function() {
    if (typeof django !== "undefined" && typeof django.jQuery !== "undefined") {
        // Estás en el entorno de administración de Django
        django.jQuery(document).ready(function () {
            var esModeradaInput = django.jQuery("#id_esModerada");
            var autoresPermitidosInput = django.jQuery("#id_autores_permitidos");

            if (esModeradaInput.length > 0) {
                var esModerada = esModeradaInput.prop('checked');
                var autoresPermitidosDisabled = esModerada ? true : false;

                esModeradaInput.prop('checked', esModerada);
                autoresPermitidosInput.prop('disabled', autoresPermitidosDisabled);

                esModeradaInput.change(function () {
                    if (django.jQuery(this).prop('checked')) {
                        autoresPermitidosInput.prop('disabled', true);
                    } else {
                        autoresPermitidosInput.prop('disabled', false);
                    }
                });
            }
        });
    } else {
        // No estás en el entorno de administración de Django, utiliza JavaScript puro
        var esModeradaInput = document.getElementById("id_esModerada");
        var autoresPermitidosInput = document.getElementById("id_autores_permitidos");

        if (esModeradaInput !== null) {
            var esModerada = esModeradaInput.checked;
            autoresPermitidosInput.disabled = esModerada;

            esModeradaInput.addEventListener("change", function () {
                var isChecked = this.checked;
                autoresPermitidosInput.disabled = isChecked;
            });
        }
    }
}, false);
