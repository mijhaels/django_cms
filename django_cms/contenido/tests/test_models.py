from django.test import TestCase

from django_cms.contenido.models import Categoria, Contenido
from django_cms.contenido.tests.factories import CategoriaFactory, ContenidoFactory


class CategoriaModelTest(TestCase):
    def setUp(self):
        self.categoria = CategoriaFactory()
        self.categoria.save()

    def test_categoria_creation(self):
        self.assertIsInstance(self.categoria, Categoria)
        self.assertEqual(self.categoria.__str__(), self.categoria.titulo)


class ContenidoModelTest(TestCase):
    def setUp(self):
        self.contenido = ContenidoFactory()
        self.contenido.save()

    def test_contenido_creation(self):
        self.assertIsInstance(self.contenido, Contenido)
        self.assertEqual(self.contenido.__str__(), self.contenido.titulo)
