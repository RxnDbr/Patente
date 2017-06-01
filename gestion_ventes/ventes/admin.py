from django.contrib import admin
from .models import *
from datetime import date

# Register your models here.

class MembreAdmin(admin.ModelAdmin):
    list_display = ('idMembre', 'nom', 'prenom', 'courriel','telephone', 'cp')
#    list_filter = ('cp',)
    date_hierarchy = 'dateAdh'
    ordering = ('idMembre',)
    search_field = ('idMembre','nom', 'prenom', 'courriel', 'cp')

class VenteAdmin(admin.ModelAdmin):
    fields=('noVente','item','noTrans','prixHTVendu')
    list_display = ('noVente','item', 'get_client','get_payee', 'get_dateFin','prixHTVendu')
#    list_filter=('item__nom',)
    search_fields = ('noTrans__client__courriel','noTrans__client__nom', 'noTrans__client__prenom')

    def get_client(self, obj):
        return obj.noTrans.client.courriel

    get_client.short_description = 'Client'
    get_client.admin_order_field = 'client__courriel'
    
    def get_payee(self, obj):
        return obj.noTrans.payee
    
    def get_dateFin(self,obj):
        date = obj.item.dateFinValidite(obj)
        return date
    
    
class TaxesAdmin(admin.ModelAdmin):
    list_diplay = ('tps','tvq')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('noTrans','client','dateTrans','vendeur', 'payee')
    list_filter = ('dateTrans', 'payee', 'vendeur',)
    search_fields = ('client__courriel','client__nom', 'client__prenom')
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('noRef','nom','prixHT')

admin.site.register(Membre, MembreAdmin)
admin.site.register(Vente)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Taxes, TaxesAdmin)

admin.site.register(Item)
admin.site.register(Adhesion, ItemAdmin)
admin.site.register(AbonnementAtelier, ItemAdmin)
admin.site.register(Entreposage, ItemAdmin)
admin.site.register(Materiel, ItemAdmin)
admin.site.register(Formation, ItemAdmin)
admin.site.register(Client)
admin.site.register(ContributionVolontaire, ItemAdmin)
