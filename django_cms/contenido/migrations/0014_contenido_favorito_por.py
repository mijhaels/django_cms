# Generated by Django 4.2.4 on 2023-12-07 22:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenido", "0013_alter_categoria_autores_permitidos"),
    ]

    operations = [
        migrations.AddField(
            model_name="contenido",
            name="favorito_por",
            field=models.ManyToManyField(blank=True, related_name="contenidos_favoritos", to=settings.AUTH_USER_MODEL),
        ),
    ]
