from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from django_cms.contenido.models import Categoria, Contenido
from django_cms.users.tests.factories import UserFactory


class CategoriaFactory(DjangoModelFactory):
    titulo = Faker("sentence")
    alias = Faker("word")
    activo = Faker("boolean")
    esModerada = Faker("boolean")

    class Meta:
        model = Categoria
        django_get_or_create = ["titulo"]


class ContenidoFactory(DjangoModelFactory):
    titulo = Faker("sentence")
    contenido = Faker("paragraph")
    fechaCreacion = Faker("date_time")
    fechaVencimiento = Faker("date_time", end_datetime=None)
    activo = Faker("boolean")
    esPublico = Faker("boolean")
    estado = Faker("random_int", min=1, max=5)
    autor = SubFactory(UserFactory)
    categoria = SubFactory(CategoriaFactory)

    class Meta:
        model = Contenido
        django_get_or_create = ["titulo"]
