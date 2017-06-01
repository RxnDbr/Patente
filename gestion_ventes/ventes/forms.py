from django import forms
from .models import Vente, Transaction, Item

class VenteForm(forms.ModelForm):
#    l_sc = Item.__subclasses__() #liste de sous classes d'Item
    CHOICES = ((None,'------'),)
    for it in Item.objects.all():
        CHOICES+=((it.noRef,it),)
    item = forms.ChoiceField(choices=CHOICES)   
    class Meta:
        model = Vente
        fields = ('noVente','prixHTVendu')

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('moyenPaiement','vendeur')
        
class ChoixTransForm(forms.Form):
    CHOICES = ()
    for trans in Transaction.objects.all().order_by('-dateTrans'):
        CHOICES+=((trans.noTrans, trans),)
    transaction = forms.ChoiceField(choices=CHOICES)
