# Generated by Django 3.2.5 on 2021-07-24 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("controlpanel", "0015_temp"),
    ]

    operations = [
        migrations.AddField(
            model_name="tile",
            name="ocean",
            field=models.BooleanField(default=False),
        ),
    ]
