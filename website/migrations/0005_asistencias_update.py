# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 04:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20160627_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencias',
            name='update',
            field=models.DateField(auto_now=True, default=datetime.datetime(2016, 7, 12, 4, 20, 29, 466065, tzinfo=utc)),
            preserve_default=False,
        ),
    ]