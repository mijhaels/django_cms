# Generated by Django 4.2.4 on 2023-10-17 13:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contenido", "0011_alter_contenido_change_reason_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="contenido",
            name="resumen",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalcontenido",
            name="resumen",
            field=models.TextField(blank=True, null=True),
        ),
    ]
