# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-08 21:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0047_auto_20170608_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('item_ptr', models.OneToOneField(default=5, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item')),
            ],
            bases=('ventes.item',),
        ),
        migrations.AlterField(
            model_name='formation',
            name='item_ptr',
            field=models.OneToOneField(default=6, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='prixHT',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Prix HT'),
        ),
        migrations.AlterField(
            model_name='vente',
            name='prixHTVendu',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Prix de vente HT'),
        ),
    ]