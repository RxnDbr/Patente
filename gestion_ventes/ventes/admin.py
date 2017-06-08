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
                .order_by(content_type_id_field, object_id_field)\
                .values_list(content_type_id_field, object_id_field).distinct()
            return [
                (
                    '{1}{0.separator}{2}'.format(self, *content_type_and_obj_id_pair),
                    ContentType.objects
                        .get(id=content_type_and_obj_id_pair[0])
                        .model_class()
                        .objects.get(pk=content_type_and_obj_id_pair[1])
                        .__str__()
                )
                for content_type_and_obj_id_pair
                in qs
            ]

        def queryset(self, request, queryset):
            try :
                content_type_id, object_id = self.value().split(self.separator)
                return queryset.filter(**({
                    content_type_id_field:content_type_id,
                    object_id_field:object_id
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
    list_display = ('membre', 'get_tel')
    def get_tel(self, obj):
        return obj.membre.telephone
        
            
class FormateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'courriel','telephone')
    
class VenteAdmin(admin.ModelAdmin):
    fields=('noVente','object_id','noTrans','prixHTVendu')
    list_display = ('noVente','content_object', 'get_client','get_payee', 'get_dateFin','prixHTVendu')
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
