from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateField
from django.urls import reverse


class User(AbstractUser):
    """
    Usuario personalizado para contentflow.
    """

    name = CharField("Nombre completo", blank=True, max_length=255)
    sex = CharField("Sexo", blank=True, max_length=1, choices=(("M", "Masculino"), ("F", "Femenino"), ("O", "Otro")))
    birth_date = DateField("Fecha de nacimiento", blank=True, null=True)

    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self) -> str:
        """Obtener URL para el detalle del usuario.

        Retorna:
            str: URL para el detalle del usuario.
        """
        return reverse("users:detail", kwargs={"username": self.username})

    def deactivate(self) -> None:
        """Desactivar usuario."""
        self.is_active = False
        self.save()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Se verifica si el usuario pertenece a alguno de los grupos especificados
        group_names = [group.name for group in self.groups.all()]
        if any(name in group_names for name in ["Autor", "Editor", "Publicador"]):
            # Si es así, se le asigna el permiso is_staff
            self.is_staff = True

        super().save(*args, **kwargs)
