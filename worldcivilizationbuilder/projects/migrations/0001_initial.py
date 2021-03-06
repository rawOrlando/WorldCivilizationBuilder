# Generated by Django 3.2.5 on 2021-07-29 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("controlpanel", "0019_auto_20210728_0130"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
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
                ("name", models.CharField(max_length=100)),
                ("spent", models.IntegerField(default=0)),
                ("last_spent", models.FloatField()),
                ("needed", models.IntegerField(blank=True, default=None, null=True)),
                (
                    "project_type",
                    models.IntegerField(
                        choices=[
                            (1, "Research Project"),
                            (2, "Exploration Project"),
                            (3, "Found Settlement Project"),
                            (4, "Region Maintance"),
                            (5, "Technology Maintance"),
                        ]
                    ),
                ),
                ("specific_project_id", models.IntegerField()),
                (
                    "civilization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects",
                        to="controlpanel.civilization",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TileMaintanceProject",
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
                ("maintaned", models.BooleanField(default=False)),
                (
                    "base_project",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
                        unique=True,
                    ),
                ),
                (
                    "tile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="maintance_project",
                        to="controlpanel.tile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TechnologyMaintanceProject",
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
                ("maintaned", models.BooleanField(default=False)),
                (
                    "base_project",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
                        unique=True,
                    ),
                ),
                (
                    "technology",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="maintance_project",
                        to="controlpanel.technology",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SettlementProject",
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
                    "base_project",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
                        unique=True,
                    ),
                ),
                (
                    "setlement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects",
                        to="controlpanel.settlement",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ResearchProject",
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
                ("technology_type", models.CharField(max_length=100)),
                (
                    "base_project",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
                        unique=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ExplorationProject",
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
                    "base_project",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
                        unique=True,
                    ),
                ),
                (
                    "territory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects",
                        to="controlpanel.tile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
