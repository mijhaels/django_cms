from django.test import TestCase
from django.urls import resolve, reverse

from django_cms.contenido.tests.factories import CategoriaFactory, ContenidoFactory
from django_cms.contenido.views import ContenidoBusquedaView, ContenidoDetalleView


class ContenidoURLsTest(TestCase):
    def setUp(self):
        self.categoria = CategoriaFactory()
        self.contenido = ContenidoFactory(categoria=self.categoria)
        self.contenido.save()

    def test_contenido_detalle_url(self):
        url = reverse("contenido:contenido_detalle", args=[self.contenido.id])
        self.assertEqual(resolve(url).func.view_class, ContenidoDetalleView)

    def test_contenido_busqueda_url(self):
        url = reverse("contenido:contenido_busqueda")
        self.assertEqual(resolve(url).func.view_class, ContenidoBusquedaView)


""" class CategoriaURLsTest(TestCase):
    def setUp(self):
        self.categoria = CategoriaFactory()

    # Add your Categoria related URL tests here
"""
