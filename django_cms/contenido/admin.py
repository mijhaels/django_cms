from django.contrib import admin
from django.shortcuts import redirect
from django_cms.users.admin import User
from simple_history.admin import SimpleHistoryAdmin
from django.utils.safestring import mark_safe

from .models import Categoria, Contenido, User
from django import forms

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['titulo', 'alias', 'activo', 'esModerada', 'autores_permitidos']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.esModerada:
            self.fields['autores_permitidos'].required = not self.instance.esModerada

    def clean(self):
        cleaned_data = super().clean()
        esModerada = cleaned_data.get('esModerada')
        autores_permitidos = cleaned_data.get('autores_permitidos')
        if not esModerada and not autores_permitidos:
            self.add_error('autores_permitidos', 'Este campo es requerido.')


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
        "editor",
        "categoria",
    )
    list_filter = ("fechaCreacion", "fechaVencimiento", "esPublico")
    search_fields = ("titulo", "autor__username", "categoria__titulo")
    readonly_fields = ("fechaCreacion", "autor","editor","publicador", "estado")

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
                    "editor",
                    "categoria",
                )
            if request.user.groups.filter(name="Editor").exists():
                obj.contenido = mark_safe(obj.contenido)
                return (
                    "fechaCreacion",
                    "fechaVencimiento",
                    "esPublico",
                    "estado",
                    "autor",
                    "editor",
                    "categoria",
                )
            if request.user.groups.filter(name="Publicador").exists():
                obj.contenido = mark_safe(obj.contenido)
                return (
                    "titulo",
                    "contenido",
                    "fechaCreacion",
                    "fechaVencimiento",
                    "activo",
                    "estado",
                    "autor",
                    "editor",
                    "publicador",
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
                    "editor",
                    "categoria",
                )
            if request.user.groups.filter(name="Editor").exists():
                obj.contenido = mark_safe(obj.contenido)
                return (
                    "fechaCreacion",
                    "fechaVencimiento",
                    "autor",
                    "editor",
                    "esPublico",
                    "estado",
                    "categoria",
                )
            if request.user.groups.filter(name="Publicador").exists():
                obj.contenido = mark_safe(obj.contenido)
                return (
                    "titulo",
                    "contenido",
                    "fechaCreacion",
                    "fechaVencimiento",
                    "activo",
                    "estado",
                    "autor",
                    "editor",
                    "publicador",
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
                    "editor",
                    "categoria",
                )
            if request.user.groups.filter(name="Editor").exists():
                obj.contenido = mark_safe(obj.contenido)
                return (
                    "fechaCreacion",
                    "fechaVencimiento",
                    "autor",
                    "editor",
                    "esPublico",
                    "estado",
                    "categoria",
                )
            if request.user.groups.filter(name="Publicador").exists():
                obj.contenido = mark_safe(obj.contenido)
                return (
                    "titulo",
                    "contenido",
                    "fechaCreacion",
                    "fechaVencimiento",
                    "activo",
                    "estado",
                    "autor",
                    "editor",
                    "publicador",
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
                    "editor",
                    "categoria",
                )
            if request.user.groups.filter(name="Editor").exists():
                obj.contenido = mark_safe(obj.contenido)
                return (
                    "fechaCreacion",
                    "fechaVencimiento",
                    "autor",
                    "editor",
                    "esPublico",
                    "estado",
                    "categoria",
                )
            if request.user.groups.filter(name="Publicador").exists():
                obj.contenido = mark_safe(obj.contenido)
                return (
                    "titulo",
                    "contenido",
                    "fechaCreacion",
                    "fechaVencimiento",
                    "activo",
                    "estado",
                    "autor",
                    "editor",
                    "publicador",
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

        if (
            request.user.groups.filter(name="Editor").exists() and contenido.estado == 2
        ):  # Si el usuario pertenece al grupo 'Editor' y el contenido está en estado 2
            extra_context["show_button_editor"] = True  
        
        if (
            request.user.groups.filter(name="Publicador").exists() and contenido.estado == 3
        ): # Si el usuario pertenece al grupo 'Publicador' y el contenido está en estado 3
            extra_context["show_button_publicador"] = True
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )


    
    def response_change(self, request, obj):
        if "_aRevision" in request.POST:  # Si se hizo clic en el botón 'Revisar'
            obj.estado = 2  # Cambia el estado a 2
            obj.save()  # Guarda el objeto
            self.message_user(request, "El contenido ha sido enviado a revisión.")  # Muestra un mensaje al usuario
            return redirect("admin:contenido_contenido_changelist")  # Redirige al usuario a la vista de lista
        
        if "_aPublicar" in request.POST:  # Si se hizo clic en el botón 'Publicar'
            obj.estado = 3  # Cambia el estado a 3
            obj.save()  # Guarda el objeto
            self.message_user(request, "El contenido ha sido enviado a publicar.")  # Muestra un mensaje al usuario
            return redirect("admin:contenido_contenido_changelist")  # Redirige al usuario a la vista de lista
        
        if "_aPublicado" in request.POST:  # Si se hizo clic en el botón 'Publicado'
            obj.estado = 4  # Cambia el estado a 4
            obj.save()  # Guarda el objeto
            self.message_user(request, "El contenido ha sido enviado a publicado.")  # Muestra un mensaje al usuario
            return redirect("admin:contenido_contenido_changelist")  # Redirige al usuario a la vista de lista
        
        if "_aRechazado" in request.POST:  # Si se hizo clic en el botón 'Rechazado'
            obj.estado = 5  # Cambia el estado a 5
            obj.save()  # Guarda el objeto
            self.message_user(request, "El contenido ha sido enviado a rechazado.")  # Muestra un mensaje al usuario
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
    form = CategoriaForm
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
    
    class Media:
        js = ('js/project.js',)
