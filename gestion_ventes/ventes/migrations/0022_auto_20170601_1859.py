# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 18:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0021_auto_20170601_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abonnementatelier',
            name='item_ptr',
            field=models.OneToOneField(default=datetime.datetime(2017, 6, 1, 18, 59, 44, 371403), on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='adhesion',
            name='item_ptr',
            field=models.OneToOneField(default=datetime.datetime(2017, 6, 1, 18, 59, 44, 374075), on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='contributionvolontaire',
            name='item_ptr',
            field=models.OneToOneField(default=datetime.datetime(2017, 6, 1, 18, 59, 44, 373301), on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='entreposage',
            name='item_ptr',
            field=models.OneToOneField(default=datetime.datetime(2017, 6, 1, 18, 59, 44, 372489), on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
    ]
