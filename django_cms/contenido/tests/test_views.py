from django.test import Client, TestCase
from django.urls import reverse

from .factories import ContenidoFactory


class ContenidoDetalleViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.contenido = ContenidoFactory.create()
        self.url = reverse("contenido:contenido_detalle", args=[self.contenido.id])

    def test_contenido_detalle_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/contenido_detalle.html")
        self.assertEqual(response.context["contenido"], self.contenido)
