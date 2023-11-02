from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django_cms.utils.storages import MediaRootS3Boto3Storage

from .models import Categoria, Contenido


class ContenidoView(View):
    def get(self, request):
        # Si el usuario inicio sesión, se obtienen los contenidos de acuerdo a si está publico o no
        if request.user.is_authenticated:
            contenido_list = Contenido.objects.filter(activo=True, estado=4).order_by("-fechaCreacion")
        # Si el usuario no inicio sesión, se obtienen los contenidos publicos
        else:
            contenido_list = Contenido.objects.filter(activo=True, esPublico=True, estado=4).order_by("-fechaCreacion")
        paginator = Paginator(contenido_list, 2)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        categorias = Categoria.objects.filter(activo=True)

        return render(request, "pages/inicio.html", {"page_obj": page_obj, "categorias": categorias})


class ContenidoDetalleView(View):
    def get(self, request, contenido_id):
        contenido = Contenido.objects.get(id=contenido_id)
        return render(request, "pages/contenido_detalle.html", {"contenido": contenido})


class ContenidoBusquedaView(View):
    def get(self, request):


        termino = None
        # Obtiene los parámetros de búsqueda

        publicacion = request.GET.get("publicacion")
        autor = request.GET.get("autor")
        categoria = request.GET.get("categoria")
        fechaCreacion = request.GET.get("fechaCreacion")
        

        # Obtiene todos los contenidos activos
        contenido_list = Contenido.objects.filter(activo=True, estado=4)

        # Si una publicación fue provista, filtra por publicación
        if publicacion is not None:
            contenido_list = contenido_list.filter(titulo__icontains=publicacion)
            termino = publicacion

        # Si un autor fue provisto, filtra por autor
        if autor is not None:
            contenido_list = contenido_list.filter(autor__username__icontains=autor)
            termino = autor

        # Si una categoría fue provista, filtra por categoría
        if categoria is not None:
            contenido_list = contenido_list.filter(categoria__titulo__icontains=categoria)
            termino = categoria

        # Si una fecha fue provista, filtra por fecha
        if fechaCreacion is not None:
            contenido_list = contenido_list.filter(fechaCreacion__fecha=fechaCreacion)

        # Ordena por fecha de creación descendente
        contenido_list = contenido_list.order_by("-fechaCreacion")

        # Continua con la paginación y renderiza la plantilla
        paginator = Paginator(contenido_list, 2)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "pages/busqueda_resultados.html", {"page_obj": page_obj, "termino": termino})


@method_decorator(csrf_exempt, name="dispatch")
class SubirImagenView(View):
    def post(self, request):
        image = request.FILES["file"]
        storage = MediaRootS3Boto3Storage()
        name = storage.save(image.name, image)
        url = storage.url(name)
        return JsonResponse({"location": url})
