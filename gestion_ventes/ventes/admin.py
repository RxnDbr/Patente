from django.contrib import admin
from .models import *
from datetime import date
from django.contrib.contenttypes.models import ContentType

def get_generic_foreign_key_filter(title, parameter_name=u'', separator='-', content_type_id_field='content_type_id', object_id_field='object_id') :
    '''
    permet d'afficher les différents types d'items vendus
    '''
    class GenericForeignKeyFilter(admin.SimpleListFilter):

        def __init__(self, request, params, model, model_admin):
            self.separator = separator
            self.title = title
            self.parameter_name = u'generic_foreign_key_' + parameter_name
            super(GenericForeignKeyFilter, self).__init__(request, params, model, model_admin)

        def lookups(self, request, model_admin):
            qs = model_admin.model.objects.all()\
                .order_by(content_type_id_field)\
                .values_list(content_type_id_field).distinct()
            return [
                (
                    '{1}{0.separator}'.format(self, *content_type_and_obj_id_pair),
                    ContentType.objects
                        .get(id=content_type_and_obj_id_pair[0])
                        .model_class().__name__
                )
                for content_type_and_obj_id_pair
                in qs
            ]

        def queryset(self, request, queryset):
            try :
                content_type_id, object_id = self.value().split(self.separator)
                return queryset.filter(**({
                    content_type_id_field:content_type_id,
                }))
            except:
                return queryset

    return GenericForeignKeyFilter
    
###########################################################
########### TOUT CE QUI CONCERNE LES VISITES ##############
###########################################################
        
class VisiteAdmin(admin.ModelAdmin):
    list_display = ('date','client','benevole','raison', 'commentaire')
    search_fields = ('client__nom', 'client__prenom', 'client__courriel', 'commentaire')
    list_filter = ('benevole','raison')
    date_hierarchy = 'date'
    
###########################################################
########### TOUT CE QUI CONCERNE LES GENS   ###############
###########################################################
            
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom','courriel')
    search_fields = ('nom','prenom','courriel')
    ordering = ('nom','prenom' )    


class MembreAdmin(admin.ModelAdmin):
    list_display = ('idMembre', 'client','telephone', 'cp')
    date_hierarchy = 'dateAdh'
    ordering = ('client__nom','idMembre',)
    search_fields = ('idMembre','client__nom', 'client__prenom', 'client__courriel', 'cp')

    
class BenevoleAdmin(admin.ModelAdmin):
    list_display = ('membre', 'get_tel', 'get_rabais', 'disponibilites')
    search_fields = ('membre__client__nom', 'membre__client__prenom', 'disponibilites','domaine1','domaine2', 'domaine3','commentaire')
    list_filter = ('domaine1',)
    ordering = ('membre__client__nom','membre__client__prenom')
    def get_tel(self, obj):
        return obj.membre.telephone
    def get_rabais(self,obj):
        return obj.compensationHeure * obj.nbHeuresCum - obj.rabaisUtilise 

class FormateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'courriel','telephone', 'get_remuneration', 'get_domaine')
    ordering = ('nom','prenom')
    
    def get_remuneration(self,obj):
        return obj.calculRemuneration()
    def get_domaine(self,obj):
        return obj.domaine1 + ', ' + obj.domaine2 + ', ' + obj.domaine3
        
        
###########################################################
########### TOUT CE QUI CONCERNE LES ITEMS ################
###########################################################        
        
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nom','prixHT', 'get_TC')
    search_fields = ('nom',)
    list_filter = ('archive',)
    ordering = ('nom', 'prixHT')
    
    def get_TC(self, obj):
        taxes = Taxes.objects.all()[0]
        return obj.calculPrixTTC(taxes)
        
class FormationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date','heure', 'formateur', 
        'jauge','get_duree', 'prixHT','get_TC')
    list_filter = ('archive', 'domaine', 'formateur__nom')
    search_fields = ('nom',)
    ordering = ('nom','date','formateur')
    
    def get_TC(self, obj):
        taxes = Taxes.objects.all()[0]
        return obj.calculPrixTTC(taxes)
        
    def get_duree(self, obj):
        return str(obj.duree_heure) + 'h' + str(obj.duree_minute)
        

###########################################################
########### TOUT CE QUI CONCERNE LES VENTES ###############
###########################################################
    
class VenteAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'get_client','get_payee', 'get_date', 'get_dateFin','prixHTVendu')
    ordering = ('noVente',)
    search_fields = ('noTrans__client__courriel','noTrans__client__nom', 'noTrans__client__prenom',)
    list_filter = (get_generic_foreign_key_filter('Articles'),'noTrans__dateTrans', 'noTrans__benevole')

    def get_client(self, obj):
        return obj.noTrans.client.nom + ' ' + obj.noTrans.client.prenom
    def get_date(self,obj):
        return obj.noTrans.dateTrans

    get_client.short_description = 'Client'
    get_client.admin_order_field = 'client__nom'
    
    def get_payee(self, obj):
        return obj.noTrans.payee
    
    def get_dateFin(self,obj):
        try:
            date = obj.content_object.dateFinValidite(obj)
        except:
            date = None
        return date
        
class TaxesAdmin(admin.ModelAdmin):
    list_display = ('get_nom','date','tps','tvq')
    ordering = ('date',)
    def get_nom(self,obj):
        return obj.__str__()

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('noTrans','client','benevole', 'get_HT', 'get_TC','payee','dateTrans')
    list_filter = ('dateTrans', 'payee', 'benevole',)
    search_fields = ('client__courriel','client__nom', 'client__prenom')
    ordering = ('noTrans','benevole','dateTrans')
        
    def get_HT(self,obj):
        prixHT = 0
        for vente in Vente.objects.filter(noTrans=obj):
            prixHT += vente.prixHTVendu
        return prixHT
    
    def get_TC(self,obj):
        prixTC = 0
        taxes = Taxes.objects.order_by('date').last()
        for vente in Vente.objects.filter(noTrans=obj):
            prixTC += vente.get_prixTCVendu(taxes)
        return prixTC

admin.site.register(Client, ClientAdmin)
admin.site.register(Membre, MembreAdmin)
admin.site.register(Benevole, BenevoleAdmin)
admin.site.register(Formateur, FormateurAdmin)

admin.site.register(Vente, VenteAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Taxes, TaxesAdmin)

admin.site.register(Item, ItemAdmin)
admin.site.register(Adhesion, ItemAdmin)
admin.site.register(AbonnementAtelier, ItemAdmin)
admin.site.register(Entreposage, ItemAdmin)
admin.site.register(Materiel, ItemAdmin)
admin.site.register(Formation, FormationAdmin)
admin.site.register(ContributionVolontaire, ItemAdmin)
admin.site.register(Services, ItemAdmin)
admin.site.register(EspaceE, ItemAdmin)
admin.site.register(BibliothequeOutils, ItemAdmin)
admin.site.register(CertificatCadeau, ItemAdmin)

admin.site.register(Visites, VisiteAdmin)
