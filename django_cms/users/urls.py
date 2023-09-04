from django.urls import path

from django_cms.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_deactivate_view,
)

app_name = "users"
urlpatterns = [
    path("~redigirir/", view=user_redirect_view, name="redirect"),
    path("~actualizar/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("~desactivar/", view=user_deactivate_view, name="deactivate_account"),
]
