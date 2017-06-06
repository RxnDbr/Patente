import csv
from datetime import datetime
from ventes import models

inp = csv.DictReader(open('ventes/membres.csv'), delimiter=',')

for membre in inp:
    c = models.Client()
    c.nom = membre['Nom']
    c.prenom = membre['Prenom']
    c.courriel = membre['Courriel']
    if len(models.Client.objects.filter(courriel=c.courriel))>0:
        c.save()    
    m = models.Membre()
    m.client = c
    m.idMembre = membre['Numero']
    m.cp = membre['Code postal']
    m.telephone = membre['Téléphone']
    m.dateAdh = datetime.strptime(membre['Date Adhésion'], '%d/%m/%Y')
    m.save()
    
