# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0034_auto_20170605_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formateur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30, verbose_name='Nom')),
                ('prenom', models.CharField(max_length=30, verbose_name='Prénom')),
                ('courriel', models.EmailField(max_length=50, verbose_name='Courriel')),
                ('telephone', models.CharField(blank=True, max_length=12, verbose_name='Numéro de téléphone')),
                ('domaine1', models.CharField(blank=True, choices=[('bois', 'bois'), ('metal', 'metal'), ('securite', 'sécurité'), ('couture', 'couture'), ('tissage', 'tissage'), ('informatique', 'informatique'), ('electronique', 'electronique'), ('art', 'art'), ('soudure', 'soudure'), ('autre', 'autre')], max_length=15, verbose_name='Domaine 1')),
                ('domaine2', models.CharField(blank=True, choices=[('bois', 'bois'), ('metal', 'metal'), ('securite', 'sécurité'), ('couture', 'couture'), ('tissage', 'tissage'), ('informatique', 'informatique'), ('electronique', 'electronique'), ('art', 'art'), ('soudure', 'soudure'), ('autre', 'autre')], max_length=15, verbose_name='Domaine 2')),
                ('domaine3', models.CharField(blank=True, choices=[('bois', 'bois'), ('metal', 'metal'), ('securite', 'sécurité'), ('couture', 'couture'), ('tissage', 'tissage'), ('informatique', 'informatique'), ('electronique', 'electronique'), ('art', 'art'), ('soudure', 'soudure'), ('autre', 'autre')], max_length=15, verbose_name='Domaine 3')),
                ('compensationHeure', models.DecimalField(decimal_places=2, default=20.0, max_digits=4)),
                ('nbHeuresCum', models.IntegerField(verbose_name="Nombre d'heures de bénévolat cumulées")),
                ('desc', models.TextField(verbose_name="Description de l'expérience")),
            ],
        ),
    ]
