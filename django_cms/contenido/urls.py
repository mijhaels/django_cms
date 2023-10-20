from django.urls import path

from .views import ContenidoBusquedaView, ContenidoDetalleView

app_name = "contenido"  # Define el app_name aquí

urlpatterns = [
    path("<int:contenido_id>/", ContenidoDetalleView.as_view(), name="contenido_detalle"),
    path("busqueda", ContenidoBusquedaView.as_view(), name="contenido_busqueda"),
]