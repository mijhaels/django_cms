from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "django_cms.users"
    verbose_name = "Usuarios"

    def ready(self):
        try:
            import django_cms.users.signals  # noqa: F401
        except ImportError:
            pass
