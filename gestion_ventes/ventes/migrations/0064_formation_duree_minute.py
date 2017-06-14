# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-14 13:49
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0063_remove_formation_duree_minute'),
    ]

    operations = [
        migrations.AddField(
            model_name='formation',
            name='duree_minute',
            field=models.IntegerField(default=30, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(60)], verbose_name='Durée de la formation en minute'),
        ),
    ]
