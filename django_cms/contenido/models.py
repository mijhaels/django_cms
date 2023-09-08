from django.db import models
from tinymce.models import HTMLField
from django_cms.users.models import User

class Contenido(models.Model):
    titulo = models.CharField(max_length=255, blank=False, null=False, verbose_name="Título") #: Titulo del contenido
    contenido = HTMLField(blank=False, null=False, verbose_name="Descripción del contenido") #: Contenido de la publicación
    fechaCreacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación") #: Fecha de creación del contenido
    fechaVencimiento = models.DateTimeField(verbose_name="Fecha de vencimiento") #: Fecha de vencimiento del contenido
    esPublico = models.BooleanField(default=True, verbose_name="¿Es público?") #: ¿Es público?
    estados = [
        (1, 'Borrador'),
        (2, 'Revisión'),
        (3, 'A publicar'),
        (4, 'Publicado'),
        (5, 'Rechazado'),
        (6, 'Inactivo')
    ]
    estado = models.IntegerField(choices=estados, default=1) #: Estado del contenido
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='autor') #: Autor del contenido
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='categoria') #: Categoria del contenido

    def __str__(self):
        return self.titulo
    
class Categoria(models.Model):
    """
    Categorías de contenidos en contentflow.
    
    """    
    titulo = models.CharField(max_length=255, blank=False, null=False, verbose_name="Título") #: Titulo de la categoria
    alias = models.CharField(max_length=255, blank=False, null=False, verbose_name="Alias") #: Alias de la categoria
    esModerada = models.BooleanField(default=False, verbose_name="¿Es moderada?") #: ¿Es moderada?

    def __str__(self):
        return self.titulo


