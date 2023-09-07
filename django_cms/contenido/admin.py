from django.contrib import admin
from .models import Contenido
from .models import Categoria

admin.site.register(Contenido)
admin.site.register(Categoria)