from django import forms
from django.contrib import admin
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin

from .models import Categoria, Contenido


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["titulo", "alias", "activo", "esModerada", "autores_permitidos"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "autores_permitidos" in self.fields:
            self.fields["autores_permitidos"].required = not self.instance.esModerada

    def clean(self):
        cleaned_data = super().clean()
        esModerada = cleaned_data.get("esModerada")
        autores_permitidos = cleaned_data.get("autores_permitidos")
        if not esModerada and not autores_permitidos:
            self.add_error("autores_permitidos", "Este campo es requerido.")

        if self.instance.esModerada:
            self.fields["autores_permitidos"].required = not self.instance.esModerada


class ContenidoAdminForm(forms.ModelForm):
    change_reason = forms.CharField(max_length=100, required=False, label="Agregar comentario")
    resumen = forms.CharField(widget=forms.Textarea, label="Resumen del contenido")

    class Meta:
        model = Contenido
        fields = "__all__"


@admin.register(Contenido)
class ContenidoAdmin(SimpleHistoryAdmin):
    form = ContenidoAdminForm
    fields = (
        "titulo",
        "resumen",
        "contenido",
        "categoria",
        "fechaCreacion",
        "fechaVencimiento",
        "activo",
        "esPublico",
        "estado",
        "autor",
        "editor",
        "publicador",
        "change_reason",
    )
    list_filter = ("fechaCreacion", "fechaVencimiento", "esPublico")
    search_fields = ("titulo", "autor__username", "categoria__titulo")
    readonly_fields = ("fechaCreacion", "autor", "editor", "publicador", "estado")
    history_list_display = ["estado"]

    def estado(self, obj):
        return obj.get_estado_display()

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        change_list = response.context_data["cl"]
        queryset = change_list.queryset
        user_groups = request.user.groups.values_list("name", flat=True)

        if "Autor" in user_groups:
            queryset = queryset.filter(autor=request.user)
        elif "Editor" in user_groups:
            queryset = queryset.filter(Q(editor=request.user) | Q(estado=2))
        elif "Publicador" in user_groups:
            queryset = queryset.filter(Q(publicador=request.user) | Q(estado=3))
        kanban_board_elements = {
            nombre_estado: list(filter(lambda content: content.estado == estado and content.activo, queryset))
            for estado, nombre_estado in Contenido.estados
        }
        extra_context = extra_context or {}
        extra_context["kanban_board_elements"] = kanban_board_elements
        return super().changelist_view(request, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        groups = request.user.groups.values_list("name", flat=True)
        readonly_fields = self.readonly_fields

        if not obj:
            return readonly_fields

        if obj.estado == 2 and "Editor" in groups:
            readonly_fields += (
                "fechaVencimiento",
                "esPublico",
                "activo",
                "categoria",
            )

        obj.contenido = mark_safe(obj.contenido)

        if obj.estado == 3 and "Publicador" in groups:
            readonly_fields += (
                "titulo",
                "resumen",
                "contenido",
                "fechaVencimiento",
                "esPublico",
                "activo",
                "categoria",
            )

        return readonly_fields

    def has_change_permission(self, request, obj=None):
        groups = request.user.groups.values_list("name", flat=True)
        if not obj:
            return True
        if obj.estado == 1 and "Autor" in groups:
            return True
        if obj.estado == 2 and "Editor" in groups:
            return True
        if obj.estado == 3 and "Publicador" in groups:
            return True
        return False

    def revert_disabled(self, request, obj=None):
        groups = request.user.groups.values_list("name", flat=True)
        history = getattr(obj, "_history", None)
        estado = getattr(history, "estado", None)
        if not obj:
            return False
        if obj.estado == 1 and "Autor" in groups and estado == 1:
            return False
        if obj.estado == 2 and "Editor" in groups and estado == 2:
            return False
        return True

    def contenido_display(self, obj):
        return mark_safe(obj.contenido)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "categoria":
            kwargs["queryset"] = Categoria.objects.filter(Q(autores_permitidos=request.user) | Q(esModerada=True))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        contenido = Contenido.objects.get(pk=object_id)
        user_groups = request.user.groups.values_list("name", flat=True)

        if "Autor" in user_groups and contenido.autor != request.user:
            raise PermissionError("No tiene permiso para ver este contenido.")

        if (
            "Autor" in user_groups
            and contenido.estado == 1
            and contenido.autor in contenido.categoria.autores_permitidos.all()
        ):
            extra_context["show_button_publicar"] = True

        if (
            "Autor" in user_groups
            and contenido.estado == 1
            and contenido.autor not in contenido.categoria.autores_permitidos.all()
        ):
            extra_context["show_button_revision"] = True

        if "Editor" in user_groups and contenido.estado == 5:
            extra_context["show_button_revision"] = True

        if "Editor" in user_groups and contenido.estado == 2:
            extra_context["show_button_a_publicar"] = True

        if "Publicador" in user_groups and contenido.estado == 3:
            extra_context["show_button_publicar"] = True
            extra_context["show_button_rechazar"] = True

        if "Autor" in user_groups and contenido.estado == 5:
            extra_context["show_button_borrador"] = True

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def response_change(self, request, obj):
        actions = {
            "_aBorrador": (1, "borrador"),
            "_aRevision": (2, "revisión"),
            "_aPublicar": (3, "publicar"),
            "_aPublicado": (4, "publicado"),
            "_aRechazado": (5, "rechazado"),
        }
        for action, (estado, message) in actions.items():
            if action in request.POST:
                obj.estado = estado
                obj.save()
                self.message_user(request, f"El contenido ha sido enviado a {message}.")
                emails = [getattr(obj, role, None) for role in ['autor', 'editor', 'publicador']]
                emails = [rol.email for rol in emails if rol]

                if emails:
                    send_mail(
                        "Estado del contenido",
                        f"El contenido {obj.titulo} ha sido enviado a {message}.",
                        None,
                        emails,
                        fail_silently=False,
                    )
                return redirect("admin:contenido_contenido_changelist")
        return super().response_change(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        else:
            if obj.estado == 2:
                obj.editor = request.user
            if obj.estado == 3:
                obj.publicador = request.user
        obj._change_reason = " "
        obj.save()
        obj._change_reason = form.cleaned_data.get("change_reason")


@admin.register(Categoria)
class CategoriaAdmin(SimpleHistoryAdmin):
    form = CategoriaForm
    list_display = ("titulo", "alias", "activo", "esModerada")
    list_filter = ("activo", "esModerada")
    search_fields = ("titulo", "alias")
    actions = (
        "activar_categorias",
        "desactivar_categorias",
        "hacer_moderadas_categorias",
        "hacer_no_moderadas_categorias",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(Q(autores_permitidos=request.user) | Q(esModerada=True))

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
        js = ("js/project.js",)
