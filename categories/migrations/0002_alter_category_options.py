# Generated by Django 4.1.5 on 2023-01-15 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "categories"},
        ),
    ]