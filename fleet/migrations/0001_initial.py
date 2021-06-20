# Generated by Django 3.2.3 on 2021-06-18 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=20, unique=True)),
                ('manufacturer', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icao', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_date', models.DateTimeField()),
                ('arrival_date', models.DateTimeField()),
                ('aircraft', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='flights', to='fleet.aircraft')),
                ('arrival_airport', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='arrival_flight', to='fleet.airport')),
                ('departure_airport', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='departura_flight', to='fleet.airport')),
            ],
        ),
    ]