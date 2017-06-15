# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 14:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0069_auto_20170614_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abonnementatelier',
            name='item_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='adhesion',
            name='item_ptr',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='bibliothequeoutils',
            name='item_ptr',
            field=models.OneToOneField(default=6, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='certificatcadeau',
            name='item_ptr',
            field=models.OneToOneField(default=7, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='client',
            name='nom',
            field=models.CharField(max_length=30, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='contributionvolontaire',
            name='item_ptr',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='entreposage',
            name='item_ptr',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='espacee',
            name='item_ptr',
            field=models.OneToOneField(default=5, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='formation',
            name='item_ptr',
            field=models.OneToOneField(default=8, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='materiel',
            name='item_ptr',
            field=models.OneToOneField(default=3, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
        migrations.AlterField(
            model_name='services',
            name='item_ptr',
            field=models.OneToOneField(default=4, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ventes.Item'),
        ),
    ]