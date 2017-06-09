# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0050_auto_20170608_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date d arrivée')),
                ('raison', models.CharField(choices=[('atelier_bois', 'Utiliser l atelier bois'), ('atelier_metal', 'Utiliser l atelier metal'), ('suivre_formation', 'Suivre une formation'), ('biblio', 'Utiliser la bibliothèque d outils'), ('espace_e', 'Espace E'), ('donner', 'Faire un don a la Patente'), ('visiter', 'Visiter/Se renseigner'), ('benevoler', 'Faire du bénévolat/travailler'), ('former', 'Donner une formation'), ('autre', 'Autre')], max_length=25, verbose_name='Raison de la visite')),
                ('commentaire', models.TextField(blank=True)),
                ('benevole', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventes.Benevole')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventes.Client')),
            ],
        ),
    ]
