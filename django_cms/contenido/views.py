from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, ExpressionWrapper, F, IntegerField
from django.db.models.functions import Cast, Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django_cms.utils.storages import MediaRootS3Boto3Storage

from .models import Categoria, Contenido


class ContenidoView(View):
    def get(self, request):
        now = timezone.now()

        hace_dos_meses = now - timezone.timedelta(days=60)

        if request.user.is_authenticated:
            contenido_destacado = (
                Contenido.objects.filter(
                    activo=True, estado=4, fechaCreacion__gte=hace_dos_meses, reactions__isnull=False
                )
                .annotate(
                    rating_multiplied=Cast(F("ratings__average") * F("ratings__count"), IntegerField()),
                    comment_count=Count("comments__object_id"),
                    reaction_count=Count("reactions__reactions__reaction"),
                )
                .prefetch_related("reactions__reactions__reaction")
                .annotate(
                    total_score=ExpressionWrapper(Coalesce(F("rating_multiplied"), 0), output_field=IntegerField())
                    + ExpressionWrapper(Coalesce(F("reaction_count"), 0), output_field=IntegerField())
                    + ExpressionWrapper(Coalesce(F("comment_count"), 0), output_field=IntegerField())
                )
                .filter(total_score__gte=3)
                .order_by("-total_score", "-fechaCreacion")
            )
        else:
            contenido_destacado = (
                Contenido.objects.filter(
                    activo=True, estado=4, esPublico=True, fechaCreacion__gte=hace_dos_meses, reactions__isnull=False
                )
                .annotate(
                    rating_multiplied=Cast(F("ratings__average") * F("ratings__count"), IntegerField()),
                    comment_count=Count("comments__object_id"),
                    reaction_count=Count("reactions__reactions__reaction"),
                )
                .prefetch_related("reactions__reactions__reaction")
                .annotate(
                    total_score=ExpressionWrapper(Coalesce(F("rating_multiplied"), 0), output_field=IntegerField())
                    + ExpressionWrapper(Coalesce(F("reaction_count"), 0), output_field=IntegerField())
                    + ExpressionWrapper(Coalesce(F("comment_count"), 0), output_field=IntegerField())
                )
                .filter(total_score__gte=3)
                .order_by("-total_score", "-fechaCreacion")
            )

        if request.user.is_authenticated:
            contenido_no_destacado = (
                Contenido.objects.filter(
                    activo=True,
                    estado=4,
                )
                .exclude(id__in=contenido_destacado.values_list("id", flat=True))
                .order_by("-fechaCreacion")
            )
        else:
            contenido_no_destacado = (
                Contenido.objects.filter(activo=True, estado=4, esPublico=True)
                .exclude(id__in=contenido_destacado.values_list("id", flat=True))
                .order_by("-fechaCreacion")
            )

        contenido_list = list(contenido_destacado) + list(contenido_no_destacado)

        paginator = Paginator(contenido_list, 4)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        categorias = Categoria.objects.filter(activo=True)

        return render(request, "pages/inicio.html", {"page_obj": page_obj, "categorias": categorias})


class ContenidoDetalleView(View):
    def get(self, request, contenido_id):
        contenido = Contenido.objects.get(id=contenido_id)
        return render(request, "pages/contenido_detalle.html", {"contenido": contenido})


class ContenidoFavoritosView(View):
    def get(self, request):
        # Obtén los contenidos marcados como favoritos por el usuario actual
        contenido_list = request.user.contenidos_favoritos.all()

        # Ordena por fecha de creación descendente
        contenido_list = contenido_list.order_by("-fechaCreacion")

        # Continua con la paginación y renderiza la plantilla
        paginator = Paginator(contenido_list, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "pages/favoritos_resultados.html", {"page_obj": page_obj})


@login_required
def favorito(request, contenido_id):
    contenido = Contenido.objects.get(id=contenido_id)
    if request.user in contenido.favorito_por.all():
        contenido.favorito_por.remove(request.user)
    else:
        contenido.favorito_por.add(request.user)
    return JsonResponse({"favorito": request.user in contenido.favorito_por.all()})


@login_required
def es_favorito(request, contenido_id):
    contenido = Contenido.objects.get(id=contenido_id)
    es_favorito = request.user in contenido.favorito_por.all()
    return JsonResponse({"favorito": es_favorito})


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
