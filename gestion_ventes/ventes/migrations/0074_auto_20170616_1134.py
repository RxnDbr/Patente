# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-16 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0073_auto_20170616_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benevole',
            name='domaine1',
            field=models.CharField(choices=[('accueil', 'accueil'), ('atelier', 'projets en atelier (entretien, construction, ...)'), ('formation', 'formation'), ('informatique', 'informatique'), ('communication', 'communication'), ('admin', 'conseil administration'), ('asso', 'comité social'), ('autre', 'autre')], max_length=15, verbose_name='Fonction principale en tant que bénévole'),
        ),
        migrations.AlterField(
            model_name='benevole',
            name='domaine2',
            field=models.CharField(blank=True, choices=[('accueil', 'accueil'), ('atelier', 'projets en atelier (entretien, construction, ...)'), ('formation', 'formation'), ('informatique', 'informatique'), ('communication', 'communication'), ('admin', 'conseil administration'), ('asso', 'comité social'), ('autre', 'autre')], max_length=15, null=True, verbose_name='Autre fonction'),
        ),
        migrations.AlterField(
            model_name='formateur',
            name='domaine1',
            field=models.CharField(blank=True, choices=[('securte', 'initiation à la Patente'), ('bois', 'bois'), ('metal', 'metal'), ('textile', 'textile'), ('informatique', 'informatique'), ('electronique', 'electronique'), ('divers', 'divers')], max_length=15, verbose_name='Domaine 1'),
        ),
        migrations.AlterField(
            model_name='formateur',
            name='domaine2',
            field=models.CharField(blank=True, choices=[('securte', 'initiation à la Patente'), ('bois', 'bois'), ('metal', 'metal'), ('textile', 'textile'), ('informatique', 'informatique'), ('electronique', 'electronique'), ('divers', 'divers')], max_length=15, verbose_name='Domaine 2'),
        ),
        migrations.AlterField(
            model_name='formateur',
            name='domaine3',
            field=models.CharField(blank=True, choices=[('securte', 'initiation à la Patente'), ('bois', 'bois'), ('metal', 'metal'), ('textile', 'textile'), ('informatique', 'informatique'), ('electronique', 'electronique'), ('divers', 'divers')], max_length=15, verbose_name='Domaine 3'),
        ),
        migrations.AlterField(
            model_name='formation',
            name='jauge',
            field=models.IntegerField(default=5, verbose_name='Nombre de participants max'),
        ),
    ]
