# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 15:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0005_auto_20170529_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abonnementatelier',
            name='item_ptr',
            field=models.OneToOneField(default=datetime.datetime(2017, 5, 29, 15, 36, 18, 844102), on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='adhesion',
            name='item_ptr',
            field=models.OneToOneField(default=datetime.datetime(2017, 5, 29, 15, 36, 18, 846582), on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='contributionvolontaire',
            name='item_ptr',
            field=models.OneToOneField(default=datetime.datetime(2017, 5, 29, 15, 36, 18, 845837), on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='entreposage',
            name='item_ptr',
            field=models.OneToOneField(default=datetime.datetime(2017, 5, 29, 15, 36, 18, 845018), on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
    ]
