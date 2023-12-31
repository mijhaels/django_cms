from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from django_cms.contenido.views import ContenidoView

urlpatterns = [
    path("", ContenidoView.as_view(), name="inicio"),
    path("acerca/", TemplateView.as_view(template_name="pages/acerca.html"), name="acerca"),
    # Django Admin, usar {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Gestión de usuarios
    path("usuarios/", include("django_cms.users.urls", namespace="users")),
    path("cuentas/", include("allauth.urls")),
    path("tinymce/", include("tinymce.urls")),
    path("contenido/", include("django_cms.contenido.urls", namespace="contenido")),
    path("comment/", include("comment.urls")),
    path("reaction/", include("reaction.urls")),
    path("rating/", include("rating.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Solicitud incorrecta")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permiso denegado")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Página no encontrada")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
