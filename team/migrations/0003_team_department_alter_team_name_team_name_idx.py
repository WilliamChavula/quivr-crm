# Generated by Django 4.2.4 on 2023-08-04 20:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("team", "0002_alter_team_created_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="department",
            field=models.CharField(
                choices=[
                    ("marketing", "Marketing"),
                    ("sales", "Sales"),
                    ("support", "Support"),
                ],
                default=[
                    ("marketing", "Marketing"),
                    ("sales", "Sales"),
                    ("support", "Support"),
                ],
                max_length=12,
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="name",
            field=models.CharField(max_length=128, verbose_name="Team name"),
        ),
        migrations.AddIndex(
            model_name="team",
            index=models.Index(fields=["name"], name="name_idx"),
        ),
    ]
