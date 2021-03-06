# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 20:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('ventes', '0043_remove_transaction_vendeur'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noTrans', models.CharField(help_text="20170506004 si c'est la 4ème vente de la journée du 6 mai 2017 par exemple", max_length=11, verbose_name='Numréro de transaction')),
                ('moyenPaiement', models.CharField(choices=[('DEBIT', 'Débit'), ('COMPTANT', 'Comptant'), ('LIGNE', 'En ligne')], max_length=10, verbose_name='Moyen de Paiement')),
                ('dateTrans', models.DateTimeField(auto_now_add=True, verbose_name='Date de transaction')),
                ('payee', models.BooleanField(default=False, verbose_name='Payé')),
                ('commentaire', models.TextField(blank=True, null=True, default='')),
                ('benevole', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ventes.Benevole')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventes.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('noVente', models.CharField(help_text="rajouter le numero d'item de la transaction au numero de transaction", max_length=13, primary_key=True, serialize=False, verbose_name='Numéro de vente')),
                ('prixHTVendu', models.DecimalField(decimal_places=3, max_digits=6, verbose_name='Prix de vente HT')),
                ('object_id', models.CharField(max_length=6, verbose_name='Référence Article')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('noTrans', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventes.Transaction')),
            ],
        ),
    ]
