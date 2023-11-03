from comment.models import Comment
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from rating.models import Rating
from reaction.models import Reaction
from simple_history.models import HistoricalRecords
from tinymce.models import HTMLField

from django_cms.users.models import User


class Contenido(models.Model):
    titulo = models.CharField(max_length=255, blank=False, null=False, verbose_name="Título")  #: Título del contenido
    resumen = models.TextField(blank=True, null=True)  #: Resumen del contenido
    contenido = HTMLField(
        blank=False, null=False, verbose_name="Descripción del contenido"
    )  #: Contenido de la publicación
    comments = GenericRelation(Comment)  #: Comentarios del contenido
    reactions = GenericRelation(Reaction)  #: Reacciones del contenido
    ratings = GenericRelation(Rating)  #: Calificaciones del contenido
    fechaCreacion = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )  #: Fecha de creación del contenido
    fechaVencimiento = models.DateTimeField(
        verbose_name="Fecha de vencimiento", blank=True, null=True
    )  #: Fecha de vencimiento del contenido
    activo = models.BooleanField(default=True, verbose_name="¿Está activo?")  #: ¿Está activo el contenido?
    esPublico = models.BooleanField(default=True, verbose_name="¿Es público?")  #: ¿Es público el contenido?
    estados = [
        (1, "Borrador"),
        (2, "Revisión"),
        (3, "A publicar"),
        (4, "Publicado"),
        (5, "Rechazado"),
    ]  #: Estados del contenido
    estado = models.IntegerField(choices=estados, default=1)  #: Estado del contenido
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="autor")  #: Autor del contenido
    editor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="editor", blank=True, null=True
    )  #: Editor del contenido
    publicador = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="publicador", blank=True, null=True
    )  #: Publicador del contenido
    historial = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True)
    )  #: Historial de cambios del contenido
    change_reason = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Agregar comentario"
    )  #: Comentario de cambio del contenido
    categoria = models.ForeignKey(
        "Categoria", on_delete=models.CASCADE, related_name="categoria"
    )  #: Categoría del contenido

    def __str__(self):
        return self.titulo


class Categoria(models.Model):
    titulo = models.CharField(
        max_length=255, blank=False, null=False, verbose_name="Título"
    )  #: Título de la categoría
    alias = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        verbose_name="Alias",
        help_text="Ejemplo: 'Ingeniería de Software II' -> 'is2'",
    )  #: Alias de la categoría
    activo = models.BooleanField(default=True, verbose_name="¿Está activo?")  #: ¿Está activa la categoría?
    esModerada = models.BooleanField(default=True, verbose_name="¿Es moderada?")  #: ¿Es moderada la categoría?
    historial = HistoricalRecords()  #: Historial de cambios de la categoría
    autores_permitidos = models.ManyToManyField(
        User, related_name="categorias_autorizadas", blank=True
    )  #: Autores permitidos para publicar en la categoría

    def save(self, *args, **kwargs):
        """Valida que no se pueda desactivar una categoría que tenga contenidos activos."""
        if not self.activo:
            contenidos_activos = Contenido.objects.filter(categoria=self, activo=True)
            if contenidos_activos.exists():
                raise ValidationError(
                    "No se puede desactivar una categoría que tenga contenidos activos.",
                    code="categoria_con_contenidos_activos",
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
