# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 19:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0040_auto_20170606_1640'),
    ]

    operations = [
        migrations.DeleteModel(name='Membre'),
        migrations.DeleteModel(name='Benevole')
        ]
