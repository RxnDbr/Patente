from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ventes$',views.faire_vente, name='faire_vente'),
    url(r'^transactions$', views.ajouter_transaction, name='ajouter_transaction'),
    url(r'^modifier_transaction$', views.modifier_transaction, name='modifier_transaction'),
    url(r'^balance$', views.balance_journee, name='balance_journee')
    
]

