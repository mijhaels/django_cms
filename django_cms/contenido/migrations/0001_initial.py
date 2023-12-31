# Generated by Django 4.2.4 on 2023-09-06 00:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contenido",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=255, verbose_name="Título")),
                ("contenido", tinymce.models.HTMLField(verbose_name="Descripción del contenido")),
                ("fechaCreacion", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("fechaVencimiento", models.DateTimeField(verbose_name="Fecha de vencimiento")),
                ("esPublico", models.BooleanField(default=True, verbose_name="¿Es público?")),
                (
                    "estado",
                    models.IntegerField(
                        choices=[
                            (1, "Borrador"),
                            (2, "Revisión"),
                            (3, "A publicar"),
                            (4, "Publicado"),
                            (5, "Rechazado"),
                            (6, "Inactivo"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "autor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="autor", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
