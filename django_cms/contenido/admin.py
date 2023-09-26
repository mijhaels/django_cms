from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Count
from simple_history.admin import SimpleHistoryAdmin

from .models import Categoria, Contenido


@admin.register(Contenido)
class ContenidoAdmin(SimpleHistoryAdmin):
    list_display = (
        "titulo",
        "fechaCreacion",
        "fechaVencimiento",
        "activo",
        "esPublico",
        "estado",
        "autor",
        "categoria",
    )
    list_filter = ("fechaCreacion", "fechaVencimiento", "activo", "esPublico", "estado", "autor", "categoria")
    search_fields = (
        "titulo",
        "fechaCreacion",
        "fechaVencimiento",
        "activo",
        "esPublico",
        "estado",
        "autor",
        "categoria",
    )
    readonly_fields = ("fechaCreacion",)
    actions = ("activar_contenidos", "desactivar_contenidos", "hacer_publicos_contenidos", "hacer_privados_contenidos")

    def changelist_view(self, request, extra_context=None):
        # Crea un diccionario donde cada estado es una clave y los contenidos son los valores
        kanban_board_elements = {
            nombre_estado: Contenido.objects.filter(estado=estado) for estado, nombre_estado in Contenido.estados
        }
        # Añade el diccionario al contexto
        extra_context = extra_context or {}
        extra_context["kanban_board_elements"] = kanban_board_elements
        return super().changelist_view(request, extra_context=extra_context)

    @admin.action(description="Activar contenido/s seleccionado/s")
    def activar_contenidos(self, request, queryset):
        queryset.update(activo=True)
        if queryset.count() == 1:
            self.message_user(request, "El contenido seleccionado ha sido activado.")
        else:
            self.message_user(request, "Los contenidos seleccionados han sido activados.")

    @admin.action(description="Desactivar contenido/s seleccionado/s")
    def desactivar_contenidos(self, request, queryset):
        queryset.update(activo=False)
        if queryset.count() == 1:
            self.message_user(request, "El contenido seleccionado ha sido desactivado.")
        else:
            self.message_user(request, "Los contenidos seleccionados han sido desactivados.")

    @admin.action(description="Hacer público/s contenido/s seleccionado/s")
    def hacer_publicos_contenidos(self, request, queryset):
        queryset.update(esPublico=True)
        if queryset.count() == 1:
            self.message_user(request, "El contenido seleccionado ha sido hecho público.")
        else:
            self.message_user(request, "Los contenidos seleccionados han sido hechos públicos.")

    @admin.action(description="Hacer privado/s contenido/s seleccionado/s")
    def hacer_privados_contenidos(self, request, queryset):
        queryset.update(esPublico=False)
        if queryset.count() == 1:
            self.message_user(request, "El contenido seleccionado ha sido hecho privado.")
        else:
            self.message_user(request, "Los contenidos seleccionados han sido hechos privados.")


@admin.register(Categoria)
class CategoriaAdmin(SimpleHistoryAdmin):
    list_display = ("titulo", "alias", "activo", "esModerada")
    list_filter = ("titulo", "alias", "activo", "esModerada")
    search_fields = ("titulo", "alias", "activo", "esModerada")
    actions = (
        "activar_categorias",
        "desactivar_categorias",
        "hacer_moderadas_categorias",
        "hacer_no_moderadas_categorias",
    )

    @admin.action(description="Hacer moderada/s categoría/s seleccionada/s")
    def hacer_moderadas_categorias(self, request, queryset):
        queryset.update(esModerada=True)
        if queryset.count() == 1:
            self.message_user(request, "La categoría seleccionada ha sido hecha moderada.")
        else:
            self.message_user(request, "Las categorías seleccionadas han sido hechas moderadas.")

    @admin.action(description="Hacer no moderada/s categoría/s seleccionada/s")
    def hacer_no_moderadas_categorias(self, request, queryset):
        queryset.update(esModerada=False)
        if queryset.count() == 1:
            self.message_user(request, "La categoría seleccionada ha sido hecha no moderada.")
        else:
            self.message_user(request, "Las categorías seleccionadas han sido hechas no moderadas.")
