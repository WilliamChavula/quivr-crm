# Generated by Django 4.2.4 on 2023-08-02 20:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]
