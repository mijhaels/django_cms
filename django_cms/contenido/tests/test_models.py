from django.core.exceptions import ValidationError
from django.test import TestCase

from django_cms.contenido.models import Categoria, Contenido
from django_cms.contenido.tests.factories import CategoriaFactory, ContenidoFactory


class CategoriaModelTest(TestCase):
    def setUp(self):
        self.categoria = CategoriaFactory()
        self.categoria.save()

    def test_creacion_categoria(self):
        self.assertIsInstance(self.categoria, Categoria)
        self.assertEqual(self.categoria.__str__(), self.categoria.titulo)

    def test_desactivacion_categoria_con_contenido_activo(self):
        contenido = ContenidoFactory(categoria=self.categoria, activo=True)
        contenido.save()
        self.categoria.activo = False
        with self.assertRaises(ValidationError):
            self.categoria.save()


class ContenidoModelTest(TestCase):
    def setUp(self):
        self.contenido = ContenidoFactory()
        self.contenido.save()

    def test_creacion_contenido(self):
        self.assertIsInstance(self.contenido, Contenido)
        self.assertEqual(self.contenido.__str__(), self.contenido.titulo)
        