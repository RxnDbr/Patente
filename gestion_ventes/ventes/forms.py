from datetime import date
from functools import partial
from django import forms
from .models import Vente, Transaction, Item, Formation, Formateur

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

#permet de mettre à jour les informations quotidiennement
dateAjd = date(2017,6,13) 

class VenteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global dateAjd
        #permet de faire des modifications à tous les jours
        #mettre cette fonction ici se justifie par le fait que le form se recharge a tous les jours d utilisations
        if date.today()>dateAjd:
            dateAjd = date.today()
            #permet d archiver automatiquement les formations qui sont passées
            for formation in Formation.objects.filter(archive=False, date__lt=dateAjd):
                formation.archive=True
                formation.save()
            # permet de mettre à jour les heures de travail des formateurs en fonction des formations données
            formateurs = Formateur.objects.all()
            for formateur in formateurs:
                formateur.nbHeuresCum = formateur.calculNbHeures()
                formateur.save()
                                
        CHOICES = ((None,'------'),)
        for it in Item.objects.filter(archive=False).order_by('nom'):
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
        
class ChoixDate(forms.Form):
    date = forms.DateField(widget=DateInput(), required=False)
        
