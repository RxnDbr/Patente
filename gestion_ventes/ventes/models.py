from datetime import timedelta, datetime, date
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

itemptr = 0

###########################################################
########### TOUT CE QUI CONCERNE LES VISITES ##############
###########################################################
    
class Visites(models.Model):
    '''
    Feuille de présence pour indiquer qui vient a la patente et pourquoi
    '''
    RAISON = (
        ('atelier_bois', 'Utiliser l atelier bois'),
        ('atelier_metal', 'Utiliser l atelier metal'),
        ('suivre_formation', 'Suivre une formation'),
        ('biblio', 'Utiliser la bibliothèque d outils'),
        ('espace_e', 'Espace E'),
        ('donner', 'Faire un don a la Patente'),
        ('visiter', 'Visiter/Se renseigner'),
        ('benevoler', 'Faire du bénévolat/travailler'),
        ('former', 'Donner une formation'),
        ('autre', 'Autre'))
        
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date d arrivée")
    benevole = models.ForeignKey('Benevole', verbose_name='Bénévole à l\'accueil')
    client = models.ForeignKey('Client')
    raison = models.CharField(max_length=25,choices=RAISON, verbose_name='Raison de la visite')
    commentaire = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.client.__str__()
        
    class Meta:
        verbose_name_plural = 'Présences'
        
        
###########################################################
########### TOUT CE QUI CONCERNE LES GENS   ###############
###########################################################
                                
class Client(models.Model):
    ''' 
    Le client est identifié par son nom, prénom et courriel
    afin de pouvoir le contacter si besoin (notamment pour des cas 
    de fin d'abonnement, etc.)
    '''
    nom = models.CharField(max_length=30, verbose_name='Nom')
    prenom = models.CharField(max_length=30, verbose_name='Prénom')
    courriel = models.EmailField(max_length=50, verbose_name='Courriel')
    
    def __str__(self):
        return self.nom + ' ' + self.prenom + '--' + self.courriel
        
                                    
class Membre(models.Model):
    '''
    Tout membre est un client qui a au moins acheté un membership
    '''
    client = models.ForeignKey('Client')
    #idMembre calculé à partir de la date d adhesion
    idMembre =  models.CharField(max_length=6, verbose_name='Numéro de membre', primary_key=True)
    cp = models.CharField(max_length=7, verbose_name='Code Postal', blank=True) #code postal
    telephone = models.CharField(max_length=12, verbose_name='Numéro de téléphone', blank=True)
    
    #la date d adhesion n est pas remplie automatiquement car les membres sont rentrés a poteriori
    # par la direction
    dateAdh = models.DateField(verbose_name='Date d\'Adhésion')    

    def __str__(self):
        return self.client.nom +' '+ self.client.prenom + '--' +self.client.courriel
    
class Benevole(models.Model):
    '''
    Tout bénévole doit être membre pour avoir accès à l'atelier et apporter des infos
    '''
     
    DOMAINES = (
        ('accueil', 'accueil'),
        ('atelier','projets en atelier (entretien, construction, ...)'),
        ('formation','formation'),
        ('informatique', 'informatique'),
        ('communication','communication'),
        ('admin','conseil administration'),
        ('asso','comité social'),
        ('autre','autre'),
    )    
    
    #Tous les benevoles doivent être membres
    membre = models.ForeignKey('Membre') 
    # les heures de bénévolats permettent d'accumuler de l argent virtuel qui permet d 
    #  utiliser les services gratuitement 
    compensationHeure = models.DecimalField(max_digits=6,decimal_places=2, verbose_name='Compensation à l\'heure', default=10.35)
    nbHeuresCum = models.IntegerField(verbose_name='Nombre d\'heures de bénévolat cumulées')
    rabaisUtilise = models.DecimalField(max_digits=6,decimal_places=2, verbose_name='Rabais Utilisé')
    disponibilites = models.TextField(blank=True, null=True)
    # pour avoir des renseignements sur les interets des bénévoles
    domaine1 = models.CharField(max_length=15,choices=DOMAINES, verbose_name='Fonction principale en tant que bénévole')
    domaine2 = models.CharField(max_length=15,choices=DOMAINES, verbose_name='Autre fonction', blank=True, null=True)
    domaine3 = models.TextField(verbose_name='Intérêts dans la vie/pour la patente', blank=True, null=True)
    
    commentaire = models.TextField(blank=True, null=True)
    
    
    def calculRabais(self):
        # le capital disponible du benevole correspond au nombre d heure qu il a offert à lA Patente
        # multiplié par le taux horaire, auquel on retranche l argent déjà utilisé
        return self.nbHeuresCum*self.compensationHeure - self.rabaisUtilise
   
    def __str__(self):
        return self.membre.client.prenom +' '+ self.membre.client.nom 
        
class Formateur(models.Model):
    '''
    Les formateurs n'ont pas besoin d etre client/membre/benevoles, ils peuvent être totalement exterieurs
    '''
    
    DOMAINES = (
        ('securte', 'initiation à la Patente'),
        ('bois', 'bois'),
        ('metal', 'metal'),
        ('textile','textile'),
        ('informatique','informatique'),
        ('electronique', 'electronique'),
        ('divers','autre'),
    )
    
    nom = models.CharField(max_length=30, verbose_name='Nom')
    prenom = models.CharField(max_length=30, verbose_name='Prénom')
    courriel = models.EmailField(max_length=50, verbose_name='Courriel')
    
    telephone = models.CharField(max_length=12, verbose_name='Numéro de téléphone', blank=True)
    
    #domaines de formation donnees
    domaine1 = models.CharField(max_length=15,choices=DOMAINES, verbose_name='Domaine 1', blank=True)
    domaine2 = models.CharField(max_length=15,choices=DOMAINES, verbose_name='Domaine 2', blank=True)
    domaine3 = models.CharField(max_length=15,choices=DOMAINES, verbose_name='Domaine 3', blank=True)
    
    #ici ce n est pas de l argent virtuel mais de l argent à payer en cheque
    compensationHeure = models.DecimalField(max_digits=4, decimal_places=2, default=20.00)
    nbHeuresCum = models.DecimalField(max_digits=6, decimal_places=2, default=0.,
        verbose_name='Nombre d\'heures de formation cumulées')
    argentDistribue = models.DecimalField(max_digits=6,decimal_places=2, 
        verbose_name='Argent Distribué', default = 0)
    desc = models.TextField(verbose_name='Description de l\'expérience')
    
    def calculRemuneration(self):
        return self.nbHeuresCum*self.compensationHeure - self.argentDistribue  
        
    def calculNbHeures(self):
        totalFormations = Formation.objects.filter(formateur=self, date__lte=date.today())
        totalHeures = 0.0
        for formation in totalFormations:
            totalHeures+= formation.duree_heure + formation.duree_minute/60.
        return totalHeures
    
    def __str__(self):
        return self.courriel +'--'+ self.prenom + self.nom 
        
###########################################################
########### TOUT CE QUI CONCERNE LES ITEMS ################
###########################################################

class Item(models.Model):
    '''
    Rassemble tous les produits et services vendus à la Patente, 
    c est la classe mere de tous les items
    '''
    
    noRef = models.AutoField(primary_key=True)
    nom  = models.CharField(max_length=41, verbose_name='Nom de l\'article')
    prixHT = models.DecimalField(max_digits=6,decimal_places=2, verbose_name='Prix Hors Taxes')
    is_taxes = models.BooleanField(default=True, verbose_name='Taxes') #pour savoir s il l item est taxé
    archive = models.BooleanField(default=False, verbose_name='Archivé') #pour savoir si l item est encore d actualité/vendu
    
    def calculTps(self, taxes):
        '''
        pour afficher le montant de la TPS seule
        '''
        if self.is_taxes:
            tps =  self.prixHT*(taxes.tps)
        else:
            tps = 0
        return round(tps,2) #arondi à deux chiffres apres la virgule
        
    def calculTvq(self, taxes):
        '''
        pour afficher le montant de la TVQ seule
        '''
        if self.is_taxes:
            tvq =  self.prixHT*(taxes.tvq)
        else:
            tvq = 0
        return round(tvq,2) #arondi à deux chiffres apres la virgule
   
    def calculPrixTTC(self,taxes):
        ''' 
        retourne le prix sans taxes + montant tps + montant tvq 
        '''
        
        prixTTC = self.prixHT + self.calculTps(taxes) + self.calculTvq(taxes)
        return round(prixTTC,2) #arondi à deux chiffres apres la virgule
    
    def dateFinValidite(self, vente):
        '''certains item n ont pas de date de fin de validité, ce sont seulement les abonnements qui en ont
        (exemple : bibliotheque d outils, atelier, entreposage, membership, ...)
        '''
        try:
            #tous les items n ont pas de champ durée
            dateFin = vente.noTrans.dateTrans + self.duree
        except:
            dateFin = None
        return dateFin
        
    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = 'Tous les items que l\'on vend'
        
        
class AbonnementAtelier(Item):
    DUREES = (
        (timedelta(hours=4),'Soir'),
        (timedelta(days=1),'Journée'),
        (timedelta(weeks=1),'Semaine'),
        (timedelta(days=31),'Mois'),
        (timedelta(days=93),'3 Mois'),
        (timedelta(days=186),'6 Mois'),
        (timedelta(days=365),'Année'),
    )
    duree = models.DurationField(choices=DUREES, verbose_name='Durée')
    is_taxes = True

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
    is_taxes = True
    
class ContributionVolontaire(Item):
    is_taxes= False
    
    class Meta:
        verbose_name_plural = 'Contributions volontaires'
    
class Adhesion(Item):
    is_taxes = False
    duree = models.DurationField(default=timedelta(days=10000)) #infini  

    class Meta:
        verbose_name_plural = 'Adhésion à la Patente'
    
class Materiel(Item):
    is_taxes = True
    
class Services(Item):
    is_taxes = True
    
    class Meta:
        verbose_name_plural = 'Services'
        
class EspaceE(Item):
    is_taxes = True
    DUREES = (
        (timedelta(weeks=1),'Semaine'),
        (timedelta(days=31),'Mois'),
        (timedelta(days=365),'Année'),
    )
    duree = models.DurationField(choices=DUREES, verbose_name='Durée')
    
    class Meta:
        verbose_name_plural = 'Espace E'
    
class BibliothequeOutils(Item):
    is_taxes = True
    DUREES = (
        (timedelta(weeks=1),'Semaine'),
        (timedelta(days=31),'Mois'),
        (timedelta(days=365),'Année'),
    )
    duree = models.DurationField(choices=DUREES, verbose_name='Durée')
    
    class Meta:
        verbose_name_plural = 'Bibliotheque d\'outils'
    
    
class CertificatCadeau(Item):
    is_taxes = False
    
    class Meta:
        verbose_name_plural = 'Certificats cadeau'
    
    
class Formation(Item):

    DOMAINES = (
        ('bois', 'bois'),
        ('metal', 'metal'),
        ('securite', 'sécurité'),
        ('textile','textile'),
        ('informatique','informatique'),
        ('electronique', 'electronique'),
        ('divers','autre'),
    )
    
    is_taxes = True
    date = models.DateField(verbose_name='Date de la formation')
    heure = models.CharField(max_length=5, default='18h')
    formateur = models.ForeignKey('Formateur')
    cout = models.DecimalField(max_digits=6,decimal_places=2, verbose_name='Coût par personne', blank=True, null=True)
    jauge = models.IntegerField(verbose_name='Nombre de participants max', default=5)
    duree_heure = models.IntegerField(verbose_name='Durée de la formation en heure', default=2)
    duree_minute = models.IntegerField(verbose_name='Durée de la formation en minute', default=30, 
        validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    domaine = models.CharField(max_length=15, default='bois', choices=DOMAINES)  
  

###########################################################
########### TOUT CE QUI CONCERNE LES VENTES ###############
###########################################################

class Transaction(models.Model):
    '''
    La classe transaction rassemble toutes les ventes (une vente = un item)
    effectuées par un client à un moment donné
    '''
     
    PAIEMENT = (
        ('DEBIT','Débit'),
        ('COMPTANT','Comptant'),
        ('LIGNE','En ligne'),
    )
    
    #le numero de transaction (noTrans) permet de retrouver facilement les ventes associées
    noTrans = models.CharField(
        max_length=11, 
        verbose_name='Numréro de transaction',
        help_text='20170506004 si c\'est la 4ème vente de la journée du 6 mai 2017 par exemple')
        
    moyenPaiement = models.CharField(max_length=10, 
        choices=PAIEMENT, 
        verbose_name='Moyen de Paiement')
    
    # la date de transaction se remplit automatiquement
    dateTrans = models.DateTimeField(auto_now_add=True, 
                                auto_now=False,
                                verbose_name="Date de transaction")
    client = models.ForeignKey('Client')
    benevole = models.ForeignKey('Benevole', blank=True, null=True)
    
    #le booléen payee permet de sauvegarder des factures ouvertes
    payee = models.BooleanField(default=False, verbose_name='Payé')
    commentaire = models.TextField(blank=True)
    
    def get_totalHT(self):
        prixHT = 0
        for vente in Vente.objects.filter(noTrans=self):
            prixHT += vente.prixHTVendu
        return prixHT
        
    def get_totalTC(self):
        prixTC = 0
        taxes = Taxes.objects.order_by('date').last()
        for vente in Vente.objects.filter(noTrans=self):
            prixTC += vente.get_prixTCVendu(taxes)
        return prixTC

    def __str__(self):
        return self.noTrans +'--'+self.client.nom


class Vente(models.Model):  
    ''' 
    La classe vente permet d'isoler tous les items achetés
    afin de faciliter les rapports de ventes, et gérer les dates
    de validité de certains abonnements
    '''
    
    #le numero de vente est composé du numero de transaction et a comme suffixe 
    #un numero a 3 chiffres pour repertorier les différents items
    noVente = models.CharField(max_length=13, primary_key=True,
        verbose_name='Numéro de vente', 
        help_text='rajouter le numero d\'item de la transaction au numero de transaction')
        
    noTrans = models.ForeignKey('Transaction')
    
    #le prix vendu peut différer du prix de base de l item
    #en cas de rabais, d exception pour une personne ou de 
    #certificat cadeau par exemple
    prixHTVendu = models.DecimalField(max_digits=6,decimal_places=2,
        verbose_name='Prix de vente HT')
        
    # les 3 variables suivantes permettent de faire acheter plusieurs
    # type d articles (formations, abonnement, ...). 
    # L'héritage simple de Item ne permettait pas certaines fonctionnalités    
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=6, verbose_name='Référence Article')
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.content_object.nom
        
    def get_prixTCVendu(self, taxes):
        return self.prixHTVendu + self.get_tps(taxes) + self.get_tvq(taxes)
        
    def get_tps(self, taxes):
        tps = 0
        if isinstance(self.content_object, Item):
            tps += self.prixHTVendu*taxes.tps
        return tps
        
    def get_tvq(self, taxes):
        tvq = 0
        if isinstance(self.content_object, Item):
            tvq += self.prixHTVendu*taxes.tvq
        return tvq

class Taxes(models.Model):
    ''' 
    Les taxes sont stockées sous forme de classe
    afin permettre une meilleure MAJ en cas de changement
    '''
    tps = models.DecimalField(max_digits=5, decimal_places=5)
    tvq = models.DecimalField(max_digits=5, decimal_places=5)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date de transaction")

    def __str__(self):
        return 'taxe mises à jour le ' + self.date.strftime("%Y/%m/%d")

    class Meta: 
        verbose_name_plural = 'Taxes'
                                

