document.addEventListener('DOMContentLoaded', function() {
    django.jQuery(document).ready(function () {
        var esModerada = django.jQuery("#id_esModerada").prop('checked');
        var autoresPermitidosDisabled = esModerada ? true : false;
        
        django.jQuery("#id_esModerada").prop('checked', esModerada);
        django.jQuery("#id_autores_permitidos").prop('disabled', autoresPermitidosDisabled);
        
        django.jQuery("#id_esModerada").change(function () {
            if (django.jQuery(this).prop('checked')) {
                django.jQuery("#id_autores_permitidos").prop('disabled', true);
            } else {
                django.jQuery("#id_autores_permitidos").prop('disabled', false);
            }
        });
    });    
}, false);