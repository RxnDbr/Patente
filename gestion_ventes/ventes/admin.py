from django.contrib import admin
from .models import *
from datetime import date
from django.contrib.contenttypes.models import ContentType

def get_generic_foreign_key_filter(title, parameter_name=u'', separator='-', content_type_id_field='content_type_id', object_id_field='object_id') :

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
    
# Register your models here.

class MembreAdmin(admin.ModelAdmin):
    list_display = ('idMembre', 'client','telephone', 'cp')
#    list_filter = ('cp',)
    date_hierarchy = 'dateAdh'
    ordering = ('idMembre',)
    search_fields = ('idMembre','client__nom', 'client__prenom', 'client__courriel', 'cp')

    
class BenevoleAdmin(admin.ModelAdmin):
    list_display = ('membre', 'get_tel', 'get_rabais', 'disponibilites')
    search_fields = ('membre__client__nom', 'membre__client__prenom', 'disponibilites','domaine1','domaine2', 'domaine3','commentaire')
    def get_tel(self, obj):
        return obj.membre.telephone
    def get_rabais(self,obj):
        return obj.compensationHeure * obj.nbHeuresCum - obj.rabaisUtilise 
        
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom','courriel')
    search_fields = ('nom','prenom','courriel')
    ordering = ('nom','prenom' )
        
            
class FormateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'courriel','telephone')
    
class VenteAdmin(admin.ModelAdmin):
    list_display = ('noVente','content_object', 'get_client','get_payee', 'get_dateFin','prixHTVendu')
    ordering = ('noVente',)
    search_fields = ('noTrans__client__courriel','noTrans__client__nom', 'noTrans__client__prenom')
    list_filter = (get_generic_foreign_key_filter('Articles'),)

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
    list_display = ('nom','prixHT', 'get_TC')
    search_fields = ('nom',)
    list_filter = ('nom', 'archive')
    
    def get_TC(self, obj):
        taxes = Taxes.objects.all()[0]
        return obj.calculPrixTTC(taxes)
        
#def VisiteAdmin(admin.ModelAdmin):
#    list_display = ('date','benevole','client','raison')
        

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
admin.site.register(Formation, ItemAdmin)
admin.site.register(ContributionVolontaire, ItemAdmin)
admin.site.register(Services, ItemAdmin)
admin.site.register(EspaceE, ItemAdmin)
admin.site.register(BibliothequeOutils, ItemAdmin)
admin.site.register(CertificatCadeau, ItemAdmin)


admin.site.register(Visites)#, VisiteAdmin)
