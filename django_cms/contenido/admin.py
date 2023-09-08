from django.contrib import admin
from .models import Contenido
from .models import Categoria
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Contenido, SimpleHistoryAdmin)
admin.site.register(Categoria, SimpleHistoryAdmin)

