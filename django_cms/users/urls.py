from django.urls import path

from django_cms.users.views import user_delete_view, user_detail_view, user_redirect_view, user_update_view

app_name = "usuarios"
urlpatterns = [
    path("~redigirir/", view=user_redirect_view, name="redirect"),
    path("~actualizar/", view=user_update_view, name="update"),
    path("~desactivar/", view=user_delete_view, name="delete"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
