# Generated by Django 3.2.5 on 2021-07-18 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("controlpanel", "0005_switch_cordinate_system"),
    ]

    operations = [
        migrations.AddField(
            model_name="civilization",
            name="last_year_updated",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
