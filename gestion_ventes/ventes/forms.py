from datetime import date
from django import forms
from .models import Vente, Transaction, Item, Formation

class VenteForm(forms.ModelForm):
#    l_sc = Item.__subclasses__() #liste de sous classes d'Item
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for it in Item.objects.filter(archive=False):
            formation = Formation.objects.filter(noRef=it.noRef)
            if len(formation):
                if formation[0].date<date.today():
                    formation[0].archive=True
                    formation[0].save()
                    
        CHOICES = ((None,'------'),)
        for it in Item.objects.filter(archive=False):
            CHOICES+=((it.noRef,it),)
        self.fields['item'] = forms.ChoiceField(choices=CHOICES)
        self.fields['noVente'] = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Vente
        fields = ('prixHTVendu',)

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('moyenPaiement','benevole', 'commentaire')
        
class ChoixTransForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CHOICES = ()
        for trans in Transaction.objects.all().order_by('-dateTrans'):
            CHOICES+=((trans.noTrans, trans),)
        self.fields['transaction'] = forms.ChoiceField(choices=CHOICES)
        
