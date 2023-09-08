from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from .models import Contenido


class ContenidoView(View):
    def get(self, request):
        contenido_list = Contenido.objects.all().order_by("-fechaCreacion")
        paginator = Paginator(contenido_list, 2)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "pages/inicio.html", {"page_obj": page_obj})
