# Generated by Django 3.2.3 on 2021-06-21 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airport',
            name='icao',
            field=models.CharField(max_length=4, unique=True),
        ),
    ]
