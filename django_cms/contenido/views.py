from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from .models import Contenido


class ContenidoView(View):
    def get(self, request):
        contenido_list = Contenido.objects.filter(activo=True).order_by("-fechaCreacion")
        paginator = Paginator(contenido_list, 2)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "pages/inicio.html", {"page_obj": page_obj})


class ContenidoDetalleView(View):
    def get(self, request, contenido_id):
        contenido = Contenido.objects.get(id=contenido_id)
        return render(request, "pages/contenido_detalle.html", {"contenido": contenido})

class ContenidoBusquedaView(View):
    def get(self, request):
        # Obtiene los parámetros de búsqueda
        autor = request.GET.get("autor")
        categoria = request.GET.get("categoria")
        fechaCreacion = request.GET.get("fechaCreacion")

        # Obtiene todos los contenidos activos
        contenido_list = Contenido.objects.filter(activo=True)

        # Si un autor fue provisto, filtra por autor
        if autor is not None:
            contenido_list = contenido_list.filter(autor__username=autor)

        # Si una categoría fue provista, filtra por categoría
        if categoria is not None:
            contenido_list = contenido_list.filter(categoria__titulo=categoria)

        # Si una fecha fue provista, filtra por fecha
        if fechaCreacion is not None:
            contenido_list = contenido_list.filter(fechaCreacion__fecha=fechaCreacion)

        # Ordena por fecha de creación descendente
        contenido_list = contenido_list.order_by("-fechaCreacion")

        # Continua con la paginación y renderiza la plantilla
        paginator = Paginator(contenido_list, 2)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "pages/busqueda_resultados.html", {"page_obj": page_obj})
