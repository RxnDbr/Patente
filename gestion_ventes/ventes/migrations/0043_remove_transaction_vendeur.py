# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 19:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0042_transaction_benevole'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='vendeur',
        ),
        migrations.DeleteModel(name='Vente'),
        migrations.DeleteModel(name='Transaction'),
    ]
