# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coreBundle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edreams_geoId', models.IntegerField(unique=True)),
                ('code', models.CharField(max_length=3)),
                ('city', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('is_main', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=4)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edreams_geoId_in', models.IntegerField(null=True, blank=True)),
                ('edreams_geoId_out', models.IntegerField(null=True, blank=True)),
                ('price', models.FloatField(null=True)),
                ('duration_in', models.CharField(max_length=10, null=True, blank=True)),
                ('duration_out', models.CharField(max_length=10)),
                ('stops_in', models.IntegerField(null=True, blank=True)),
                ('stops_out', models.IntegerField(null=True)),
                ('trip_type', models.CharField(max_length=10, choices=[(b'ONE_WAY', b'one way'), (b'ROUND_TRIP', b'round_trip')])),
                ('date_in', models.DateTimeField()),
                ('date_out', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='CityAirport',
        ),
        migrations.AddField(
            model_name='airport',
            name='country',
            field=models.ForeignKey(to='coreBundle.Country'),
            preserve_default=True,
        ),
    ]
