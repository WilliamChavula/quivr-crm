# Generated by Django 4.2.4 on 2023-08-02 20:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("team", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="my_team",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
