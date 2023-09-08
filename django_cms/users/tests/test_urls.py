from django.urls import resolve, reverse

from django_cms.users.models import User


def test_detail(user: User):
    assert reverse("usuarios:detail", kwargs={"username": user.username}) == f"/usuarios/{user.username}/"
    assert resolve(f"/usuarios/{user.username}/").view_name == "users:detail"


def test_update():
    assert reverse("usuarios:update") == "/usuarios/~actualizar/"
    assert resolve("/usuarios/~actualizar/").view_name == "users:update"


def test_redirect():
    assert reverse("usuarios:redirect") == "/usuarios/~redirigir/"
    assert resolve("/usuarios/~redirigir/").view_name == "users:redirect"
