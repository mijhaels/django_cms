from django.urls import path

from .views import (
    ContenidoBusquedaView,
    ContenidoDetalleView,
    ContenidoFavoritosView,
    SubirImagenView,
    es_favorito,
    favorito,
)

app_name = "contenido"  # Define el app_name aquí

urlpatterns = [
    path("<int:contenido_id>", ContenidoDetalleView.as_view(), name="contenido_detalle"),
    path("busqueda", ContenidoBusquedaView.as_view(), name="contenido_busqueda"),
    path("subir", SubirImagenView.as_view(), name="subir_imagen"),
    path("favoritos/", ContenidoFavoritosView.as_view(), name="favoritos"),
    path("favorito/<int:contenido_id>/", favorito, name="favorito"),
    path("es_favorito/<int:contenido_id>/", es_favorito, name="es_favorito"),
]
