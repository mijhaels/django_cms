# Generated by Django 4.2.4 on 2023-08-25 01:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(blank=True, max_length=255, verbose_name="Nombre de usuario"),
        ),
    ]
