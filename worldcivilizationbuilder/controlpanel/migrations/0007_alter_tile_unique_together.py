# Generated by Django 3.2.5 on 2021-07-18 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controlpanel', '0006_civilization_last_year_updated'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tile',
            unique_together={('x', 'y', 'z')},
        ),
    ]
