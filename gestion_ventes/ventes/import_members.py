import csv
from datetime import datetime
from ventes import models

inp = csv.DictReader(open('ventes/membres.csv'), delimiter=',')

for membre in inp:
    m = models.Membre()
    m.nom = membre['Nom']
    m.prenom = membre['Prenom']
    m.courriel = membre['Courriel']
    m.idMembre = membre['Numero']
    m.cp = membre['Code postal']
    m.telephone = membre['Téléphone']
    m.dateAdh = datetime.strptime(membre['Date Adhésion'], '%d/%m/%Y')
    m.save()
    
