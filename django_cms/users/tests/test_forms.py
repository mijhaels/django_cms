"""
Module for all Form Tests.
"""

from django_cms.users.forms import UserAdminCreationForm
from django_cms.users.models import User


class TestUserAdminCreationForm:
    """
    Clase de prueba para todas las pruebas relacionadas con UserAdminCreationForm
    """

    def test_username_validation_error_msg(self, user: User):
        """
        Comprueba que el validador único del formulario UserAdminCreation funciona correctamente:
            1) No se puede añadir un nuevo usuario con un nombre de usuario existente.
            2) El formulario UserCreation sólo genera un error.
            3) Se muestra el mensaje de error deseado
        """

        # El usuario ya existe,
        # por lo que no se puede crear.
        form = UserAdminCreationForm(
            {
                "username": user.username,
                "password1": user.password,
                "password2": user.password,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors
        assert form.errors["username"][0] == "Este usuario ya existe"
