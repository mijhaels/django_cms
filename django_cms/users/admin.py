from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import decorators, get_user_model

from django_cms.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://django-allauth.readthedocs.io/en/stable/advanced.html#admin
    admin.site.login = decorators.login_required(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Información personal", {"fields": ("name", "email")}),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "groups",
                    "user_permissions",
                    "sex",
                    "birth_date",
                ),
            },
        ),
        ("Fechas importantes", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_active"]
    search_fields = ["name"]


admin.site.unregister(EmailAddress)


@admin.register(EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ["email", "user", "verified", "primary"]

    def get_queryset(self, request):
        qs = super(EmailAddressAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
