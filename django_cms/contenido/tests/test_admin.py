from django.urls import reverse

from django_cms.contenido.models import Categoria


class TestCategoriaAdmin:
    def test_changelist(self, admin_client):
        url = reverse("admin:contenido_categoria_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_search(self, admin_client):
        url = reverse("admin:contenido_categoria_changelist")
        response = admin_client.get(url, data={"q": "test"})
        assert response.status_code == 200

    def test_add(self, admin_client):
        url = reverse("admin:contenido_categoria_add")
        response = admin_client.get(url)
        assert response.status_code == 200

        response = admin_client.post(
            url,
            data={
                "titulo": "test",
                "alias": "test_alias",
                "activo": True,
                "esModerada": False,
            },
        )
        assert response.status_code == 302
        assert Categoria.objects.filter(titulo="test").exists()


class TestContenidoAdmin:
    def test_changelist(self, admin_client):
        url = reverse("admin:contenido_contenido_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_add(self, admin_client):
        url = reverse("admin:contenido_contenido_add")
        response = admin_client.get(url)
        assert response.status_code == 200
