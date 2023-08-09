# Generated by Django 4.2.4 on 2023-08-08 16:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0008_client_preferred_communication"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="preferred_communication",
            field=models.CharField(
                choices=[
                    ("email", "Email"),
                    ("mail", "Mail"),
                    ("phone", "Phone"),
                    ("social_media", "Social"),
                ],
                default="email",
                max_length=15,
            ),
        ),
    ]