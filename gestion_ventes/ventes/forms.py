from django import forms
from .models import Vente, Transaction

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ('noVente','item', 'prixHTVendu')

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('client','moyenPaiement','vendeur')
        
class ChoixTransForm(forms.Form):
    CHOICES = ()
    for trans in Transaction.objects.all().order_by('-dateTrans'):
        CHOICES+=((trans.noTrans, trans),)
    transaction = forms.ChoiceField(choices=CHOICES)
