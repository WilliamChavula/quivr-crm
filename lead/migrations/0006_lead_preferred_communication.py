# Generated by Django 4.2.4 on 2023-08-04 21:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lead", "0005_alter_lead_social"),
    ]

    operations = [
        migrations.AddField(
            model_name="lead",
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
            preserve_default=False,
        ),
    ]