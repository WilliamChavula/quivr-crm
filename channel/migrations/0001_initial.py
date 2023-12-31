# Generated by Django 4.2.4 on 2023-08-04 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("team", "0003_team_department_alter_team_name_team_name_idx"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Channel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "mode",
                    models.CharField(
                        choices=[
                            ("email", "Email"),
                            ("mail", "Mail"),
                            ("phone", "Phone"),
                            ("social_media", "Social"),
                        ],
                        db_index=True,
                        max_length=15,
                    ),
                ),
                ("date_contacted", models.DateTimeField()),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "team_contacting",
                    models.ForeignKey(
                        default="sales",
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="team.team",
                    ),
                ),
            ],
            options={
                "ordering": ["-date_contacted"],
                "indexes": [
                    models.Index(
                        fields=["content_type", "object_id"],
                        name="channel_cha_content_49eff8_idx",
                    )
                ],
            },
        ),
    ]
