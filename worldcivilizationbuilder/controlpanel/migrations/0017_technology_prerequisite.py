# Generated by Django 3.2.5 on 2021-07-25 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("controlpanel", "0016_tile_ocean"),
    ]

    operations = [
        migrations.AddField(
            model_name="technology",
            name="prerequisite",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="unlocks",
                to="controlpanel.technology",
            ),
        ),
    ]
