from django.contrib import admin
from django.shortcuts import redirect
from django_cms.users.admin import User
from simple_history.admin import SimpleHistoryAdmin
from django.utils.safestring import mark_safe

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
    list_filter = ("fechaCreacion", "fechaVencimiento", "esPublico")
    search_fields = ("titulo", "autor__username", "categoria__titulo")
    readonly_fields = ("fechaCreacion", "autor", "estado")

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        change_list = response.context_data["cl"]
        queryset = change_list.queryset
        # Comprobar si el usuario actual pertenece al grupo "Autor"
        if request.user.groups.filter(name="Autor").exists():
            # Si el usuario pertenece al grupo "Autor", filtrar el queryset para que solo contenga contenidos creados por el usuario actual
            queryset = queryset.filter(autor=request.user)
        kanban_board_elements = {
            nombre_estado: list(filter(lambda content: content.estado == estado and content.activo, queryset))
            for estado, nombre_estado in Contenido.estados
        }
        extra_context = extra_context or {}
        extra_context["kanban_board_elements"] = kanban_board_elements
        return super().changelist_view(request, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.estado == 1:
            if request.user.groups.filter(name="Autor").exists():
                return ("fechaCreacion", "esPublico", "autor", "estado")
        if obj and obj.estado == 2:
            if request.user.groups.filter(name="Autor").exists():
                obj.contenido = mark_safe(obj.contenido)
                return (
                    "titulo",
                    "contenido",
                    "fechaCreacion",
                    "fechaVencimiento",
                    "activo",
                    "esPublico",
                    "estado",
                    "autor",
                    "categoria",
                )
        if obj and obj.estado == 3:
            if request.user.groups.filter(name="Autor").exists():
                obj.contenido = mark_safe(obj.contenido)
                return (
                    "titulo",
                    "contenido",
                    "fechaCreacion",
                    "fechaVencimiento",
                    "activo",
                    "esPublico",
                    "estado",
                    "autor",
                    "categoria",
                )
        if obj and obj.estado == 4:
            if request.user.groups.filter(name="Autor").exists():
                obj.contenido = mark_safe(obj.contenido)
                return (
                    "titulo",
                    "contenido",
                    "fechaCreacion",
                    "fechaVencimiento",
                    "activo",
                    "esPublico",
                    "estado",
                    "autor",
                    "categoria",
                )
        if obj and obj.estado == 5:
            if request.user.groups.filter(name="Autor").exists():
                obj.contenido = mark_safe(obj.contenido)
                return (
                    "titulo",
                    "contenido",
                    "fechaCreacion",
                    "fechaVencimiento",
                    "activo",
                    "esPublico",
                    "estado",
                    "autor",
                    "categoria",
                )

        return self.readonly_fields

    def contenido_display(self, obj):
        return mark_safe(obj.contenido)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_button_autor"] = False
        contenido = Contenido.objects.get(pk=object_id)
        if request.user.groups.filter(name="Autor").exists() and contenido.autor != request.user:
            raise PermissionError("No tiene permiso para ver este contenido.")

        if (
            request.user.groups.filter(name="Autor").exists() and contenido.estado == 1
        ):  # Si el usuario pertenece al grupo 'Autor' y el contenido está en estado 1
            extra_context["show_button_autor"] = True

        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

    def response_change(self, request, obj):
        if "_revisar" in request.POST:  # Si se hizo clic en el botón 'Enviar'
            obj.estado = 2  # Cambia el estado a 2
            obj.save()  # Guarda el objeto
            self.message_user(request, "El contenido ha sido enviado a revisión.")  # Muestra un mensaje al usuario
            return redirect("admin:contenido_contenido_changelist")  # Redirige al usuario a la vista de lista
        return super().response_change(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        super().save_model(request, obj, form, change)


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
