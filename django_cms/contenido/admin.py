from django.contrib import admin
from .models import Contenido
from .models import Categoria
from tinymce.widgets import TinyMCE
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

admin.site.register(Contenido)
admin.site.register(Categoria)
admin.site.unregister(FlatPage)

class TinyMCEFlatPageAdmin(FlatPageAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
       if db_field.name == 'content':
           return db_field.formfield(widget=TinyMCE(
               attrs={'cols': 80, 'rows': 30},
               mce_attrs={'external_link_list_url': reverse('tinymce-linklist'), 'external_image_list_url': reverse('tinymce-imagelist')},
           ))
       return super().formfield_for_dbfield(db_field, **kwargs)

admin.site.register(FlatPage, TinyMCEFlatPageAdmin)       