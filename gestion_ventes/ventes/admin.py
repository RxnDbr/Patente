from django.contrib import admin
from .models import *
from datetime import date

# Register your models here.

class MembreAdmin(admin.ModelAdmin):
    list_display = ('idMembre', 'client','telephone', 'cp')
#    list_filter = ('cp',)
    date_hierarchy = 'dateAdh'
    ordering = ('idMembre',)
    search_fields = ('idMembre','client__nom', 'client__prenom', 'client__courriel', 'cp')
    
class BenevoleAdmin(admin.ModelAdmin):
    list_display = ('membre', 'get_tel')
    def get_tel(self, obj):
        return obj.membre.telephone
        
            
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
    list_display = ('noTrans','client','dateTrans','benevole', 'payee')
    list_filter = ('dateTrans', 'payee', 'benevole',)
    search_fields = ('client__courriel','client__nom', 'client__prenom')
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('noRef','nom','prixHT')

admin.site.register(Client)
admin.site.register(Membre, MembreAdmin)
admin.site.register(Benevole)#, BenevoleAdmin)
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
