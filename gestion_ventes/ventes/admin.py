from django.contrib import admin
from .models import *
from datetime import date

# Register your models here.

class MembreAdmin(admin.ModelAdmin):
    list_display = ('idMembre', 'client_nom', 'client_prenom', 'client_courriel','telephone', 'cp')
#    list_filter = ('cp',)
    fields = ('client_ptr','telephone', 'cp')
    date_hierarchy = 'dateAdh'
    ordering = ('idMembre',)
    search_fields = ('idMembre','nom', 'prenom', 'courriel', 'cp')
    
class BenevoleAdmin(admin.ModelAdmin):
    list_display = ('membre_client_prenom', 'membre_client_nom', 'membre_client_courriel', 'membre_telephone')
    
class FormateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'courriel','telephone')
    
class VenteAdmin(admin.ModelAdmin):
    fields=('noVente','content_object','noTrans','prixHTVendu')
    list_display = ('noVente','content_object', 'get_client','get_payee', 'get_dateFin','prixHTVendu')
    search_fields = ('noTrans__client__courriel','noTrans__client__nom', 'noTrans__client__prenom')
    list_filter = ('object_id',)

    def get_client(self, obj):
        return obj.noTrans.client.courriel

    get_client.short_description = 'Client'
    get_client.admin_order_field = 'client__courriel'
    
    def get_payee(self, obj):
        return obj.noTrans.payee
    
    def get_dateFin(self,obj):
        try:
            date = obj.content_object.dateFinValidite(obj)
        except:
            date = None
        return date
    
    
class TaxesAdmin(admin.ModelAdmin):
    list_diplay = ('tps','tvq')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('noTrans','client','dateTrans','vendeur', 'payee')
    list_filter = ('dateTrans', 'payee', 'vendeur',)
    search_fields = ('client__courriel','client__nom', 'client__prenom')
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('noRef','nom','prixHT')

admin.site.register(Client)
admin.site.register(Membre)
admin.site.register(Benevole)
admin.site.register(Formateur, FormateurAdmin)
admin.site.register(Vente, VenteAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Taxes, TaxesAdmin)

admin.site.register(Item)
admin.site.register(Adhesion, ItemAdmin)
admin.site.register(AbonnementAtelier, ItemAdmin)
admin.site.register(Entreposage, ItemAdmin)
admin.site.register(Materiel, ItemAdmin)
admin.site.register(Formation, ItemAdmin)
admin.site.register(ContributionVolontaire, ItemAdmin)
