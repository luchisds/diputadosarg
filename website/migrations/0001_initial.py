# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bloque', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('presente', models.IntegerField()),
                ('ausente', models.IntegerField()),
                ('licencia', models.IntegerField()),
                ('mo', models.IntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='asistencias',
            unique_together=set([('nombre', 'bloque')]),
        ),
    ]
