# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-13 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0059_auto_20170613_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='formateur',
            name='argentDistribue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Argent Distribué'),
        ),
    ]