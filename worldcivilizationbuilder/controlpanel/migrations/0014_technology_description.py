# Generated by Django 3.2.5 on 2021-07-23 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlpanel', '0013_civilization_technologies'),
    ]

    operations = [
        migrations.AddField(
            model_name='technology',
            name='description',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
