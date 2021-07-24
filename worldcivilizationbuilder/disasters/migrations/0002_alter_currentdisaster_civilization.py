# Generated by Django 3.2.5 on 2021-07-23 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controlpanel', '0014_technology_description'),
        ('disasters', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentdisaster',
            name='civilization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_disasters', to='controlpanel.civilization'),
        ),
    ]