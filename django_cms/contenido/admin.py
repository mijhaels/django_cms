from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Categoria, Contenido

admin.site.register(Contenido, SimpleHistoryAdmin)
admin.site.register(Categoria, SimpleHistoryAdmin)
