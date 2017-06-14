from datetime import date
from django import forms
from .models import Vente, Transaction, Item, Formation, Formateur


dateAjd = date.today() 

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
        
        global dateAjd
        if date.today()>dateAjd:
        
            #pour calculer le nb d heure cumulées d un formateur, je mets la fonction ici
            # pour que le calcul se reactualise a tous les jours
            
            formateurs = Formateur.objects.all()
            for formateur in formateurs:
                formateur.nbHeuresCum = formateur.calculNbHeures()
                formateur.save()
                
            dateAjd = date.today()
        	
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
        
