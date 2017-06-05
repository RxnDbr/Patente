import csv
from datetime import datetime
from ventes import models

inp = csv.DictReader(open('ventes/formateurs.csv'), delimiter=',')

for formateur in inp:
    f = models.Formateur()
    f.nom = formateur['Nom']
    f.prenom = formateur['Prénom']
    f.courriel = formateur['Courriel']
    f.telephone = formateur['Téléphone']
    f.desc = formateur['Formations données']
    f.nbHeuresCum = 0
    f.save()
    
