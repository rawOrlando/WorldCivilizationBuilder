# Generated by Django 3.2.5 on 2021-07-28 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlpanel', '0018_move_needed_maintance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technology',
            name='needed_maintance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]