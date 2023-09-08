from django.urls import resolve, reverse

from django_cms.users.models import User


def test_detail(user: User):
    assert reverse("usuarios:detail", kwargs={"username": user.username}) == f"/usuarios/{user.username}/"
    assert resolve(f"/usuarios/{user.username}/").view_name == "usuarios:detail"


def test_update():
    assert reverse("usuarios:update") == "/usuarios/~update/"
    assert resolve("/usuarios/~update/").view_name == "usuarios:update"


def test_redirect():
    assert reverse("usuarios:redirect") == "/usuarios/~redirect/"
    assert resolve("/usuarios/~redirect/").view_name == "usuarios:redirect"
