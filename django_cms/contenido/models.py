from django.db import models
from tinymce.models import HTMLField
from django_cms.users.models import User

class Contenido(models.Model):
    titulo = models.CharField(max_length=255, blank=False, null=False, verbose_name="Título")
    contenido = HTMLField(blank=False, null=False, verbose_name="Descripción del contenido")
    fechaCreacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fechaVencimiento = models.DateTimeField(verbose_name="Fecha de vencimiento")
    esPublico = models.BooleanField(default=True, verbose_name="¿Es público?")
    estados = [
        (1, 'Borrador'),
        (2, 'Revisión'),
        (3, 'A publicar'),
        (4, 'Publicado'),
        (5, 'Rechazado'),
        (6, 'Inactivo')
    ]
    estado = models.IntegerField(choices=estados, default=1)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='autor')
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='categoria')
    
class Categoria(models.Model):
    titulo = models.CharField(max_length=255, blank=False, null=False, verbose_name="Título")
    alias = models.CharField(max_length=255, blank=False, null=False, verbose_name="Alias")
    esModerada = models.BooleanField(default=False, verbose_name="¿Es moderada?")


