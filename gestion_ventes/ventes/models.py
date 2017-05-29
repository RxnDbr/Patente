from django.db import models
from datetime import timedelta, datetime

itemptr = 0

# Create your models here.

class Taxes(models.Model):
    tps = models.DecimalField(max_digits=5, decimal_places=4)
    tvq = models.DecimalField(max_digits=5, decimal_places=4)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date de transaction")
                                
class Client(models.Model):
    nom = models.CharField(max_length=30, verbose_name='Nom')
    prenom = models.CharField(max_length=30, verbose_name='Prénom')
    courriel = models.EmailField(primary_key=True,max_length=50, unique=True, verbose_name='Courriel')
    
    def __str__(self):
        return self.courriel +'--'+ self.prenom + self.nom + ' '
                                    
class Membre(Client):
    idMembre =  models.CharField(max_length=6, primary_key=True, verbose_name='Numéro de membre')
    cp = models.CharField(max_length=7, verbose_name='Code Postal')
    telephone = models.CharField(max_length=12, verbose_name='Numéro de téléphone')
    dateAdh = models.DateField(verbose_name='Date d\'Adhésion')
        
        

class Item(models.Model):
    noRef = models.CharField(max_length=6,primary_key=True, verbose_name='Référence Article')
    nom  = models.CharField(max_length=30, verbose_name='Nom de l\'article')
    prixHT = models.DecimalField(max_digits=6,decimal_places=3, verbose_name='Prix HT')
    is_taxes = models.BooleanField(default=True, verbose_name='Taxes')
    
    def calculTps(self, taxes):
        if self.is_taxes:
            tps =  self.prixHT*(taxes.tps)
        else:
            tps = 0
        return tps
        
    def calculTvq(self, taxes):
        if self.is_taxes:
            tvq =  self.prixHT*(taxes.tvq)
        else:
            tvq = 0
        return tvq
   
    def calculPrixTTC(self,taxes):
        prixTTC = self.prixHT + calculTps(taxes) + calculTvq(taxes)
        return prixTTC
        
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.noRef +' -- '+  self.nom    
    class Meta:
        abstract=False
        
        
class AbonnementAtelier(Item):
    DUREES = (
        (timedelta(hours=4),'Soir'),
        (timedelta(days=1),'Journée'),
        (timedelta(weeks=1),'Semaine'),
        (timedelta(days=31),'Mois'),
        (timedelta(days=365),'Année'),
    )
#remplir automATIQUEMENT DES CHAMPS
    duree = models.DurationField(choices=DUREES, verbose_name='Durée')
    taxes = True
    
    global itemptr
    item_ptr = models.OneToOneField(
        Item, on_delete=models.CASCADE,
        parent_link=True,
        default=datetime.now()
    )
    itemptr+=1


class Entreposage(Item):
    DUREES = (
        (timedelta(days=1),'Journée'),
        (timedelta(weeks=1),'Semaine'),
        (timedelta(days=31),'Mois'),
    )
    TAILLES = (
        ('petit','2*3'),
        ('moyen','4*3'),
        ('grand','8*3'),
    )
    duree = models.DurationField(choices=DUREES, verbose_name='Durée')
    taille = models.CharField(max_length=10,choices=TAILLES, verbose_name='Taille')
#    numero = models.IntegerField(verbose_name='Numéro')
    taxes = True
    global itemptr
    item_ptr = models.OneToOneField(
        Item, on_delete=models.CASCADE,
        parent_link=True,
        default=datetime.now()
    )
    itemptr+=1
    
class ContributionVolontaire(Item):
    taxes = False
    global itemptr
    item_ptr = models.OneToOneField(
        Item, on_delete=models.CASCADE,
        parent_link=True,
        default=datetime.now()
    )
    itemptr+=1
    
class Adhesion(Item):
    taxes = False
    global itemptr
    item_ptr = models.OneToOneField(
        Item, on_delete=models.CASCADE,
        parent_link=True,
        default=datetime.now()
    )
    itemptr+=1
    
class Materiel(Item):
    taxes = True
    global itemptr
    item_ptr = models.OneToOneField(
        Item, on_delete=models.CASCADE,
        parent_link=True,
        default=itemptr
    )
    itemptr+=1
        
class Formation(Item):
    date = models.DateField(verbose_name='Date de la formation')
    formateur = models.CharField(max_length=30, verbose_name = 'Formateur')
    cout = models.DecimalField(max_digits=6,decimal_places=2, verbose_name='Coût')
    jauge = models.IntegerField(verbose_name='Jauge')
    duree = models.DurationField(verbose_name='Durée')
    global itemptr
    item_ptr = models.OneToOneField(
        Item, on_delete=models.CASCADE,
        parent_link=True,
        default=itemptr
    )
    itemptr+=1
        
class Transaction(models.Model):
    PAIEMENT = (
        ('DEBIT','Débit'),
        ('COMPTANT','Comptant'),
        ('LIGNE','En ligne'),
    )

    noTrans = models.CharField(max_length=11, verbose_name='Numréro de transaction',
        help_text='20170506004 si c\'est la 4ème vente de la journée du 6 mai 2017 par exemple')
    moyenPaiement = models.CharField(max_length=10, choices=PAIEMENT, verbose_name='Moyen de Paiement')
    dateTrans = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date de transaction")
    client = models.ForeignKey('Client')
    vendeur = models.CharField(max_length=30)
    payee = models.BooleanField(default=False, verbose_name='Payé')

    def __str__(self):
        return self.noTrans +'--'+self.client.nom

class Vente(models.Model):
    noVente = models.CharField(max_length=13, primary_key=True, verbose_name='Numéro de vente', help_text='rajouter le numero d\'item de la transaction au numero de transaction')
    noTrans = models.ForeignKey('Transaction')
    item = models.ForeignKey('Item')
    prixHTVendu = models.DecimalField(max_digits=6,decimal_places=3,verbose_name='Prix de vente HT')

    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.noVente + '--' + self.item.nom
