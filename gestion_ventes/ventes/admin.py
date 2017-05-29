from django.contrib import admin
from .models import *

# Register your models here.

class MembreAdmin(admin.ModelAdmin):
    list_display = ('idMembre', 'nom', 'prenom', 'courriel','telephone', 'cp')
#    list_filter = ('cp',)
    date_hierarchy = 'dateAdh'
    ordering = ('idMembre',)
    search_field = ('idMembre','nom', 'prenom', 'courriel', 'cp')

class VenteAdmin(admin.ModelAdmin):
    fields=('noVente','item','noTrans','prixHTVendu')
    list_display = ('noVente','noTrans','item','prixHTVendu')

class TaxesAdmin(admin.ModelAdmin):
    list_diplay = ('tps','tvq')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('noTrans','client','dateTrans','vendeur', 'payee')
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('noRef','nom','prixHT')

admin.site.register(Membre, MembreAdmin)
admin.site.register(Vente, VenteAdmin)
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
