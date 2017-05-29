# Create your views here.
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.forms import modelformset_factory,inlineformset_factory
from django.db import IntegrityError, transaction
from .models import Client, Membre,Vente, Taxes, Transaction, Item
from .forms import VenteForm, TransactionForm, ChoixTransForm
from datetime import date

noTrans = Transaction.objects.all().last().noTrans
taxes = Taxes.objects.all().last()

    
def ajouter_transaction(request):
    global noTrans
    dateTrans = date.today()
    str_date = dateTrans.strftime("%Y%m%d")
    toutes_trans_date = Transaction.objects.filter(noTrans__contains=str_date)
    tous_no_trans_date = []
    if not toutes_trans_date:
        noTrans = str_date+'000'
    else:
        for trans in toutes_trans_date:
            tous_no_trans_date.append(trans.noTrans)
        noTrans = str(int(max(tous_no_trans_date))+1)
    if request.POST:
        return redirect(faire_vente)
    return render(request, 'ventes/transactions.html', locals())

def faire_vente(request):
    trans = Transaction.objects.filter(noTrans=noTrans)
    a = []
    if trans:
        a.append(11)
        trans = trans[0]
        initial_trans = {'client':trans.client, 'moyenPaiement':trans.moyenPaiement, 'vendeur':trans.vendeur}
    else:
        a.append(12)
        trans = Transaction(noTrans=noTrans, client=Client.objects.all()[0], moyenPaiement='', vendeur='')
        trans.save() 
        initial_trans =  {'client':None, 'moyenPaiement':None, 'vendeur':None}
    
    #MANAGE INITIAL DISPLAY  
    ventes_trans = Vente.objects.filter(noTrans=trans)
    ventes_data = []
    totalPrixHT = totalTps = totalTvq = 0
    for vente in ventes_trans:
        ventes_data.append({'item':vente.item, 'noVente':vente.noVente, 'prixHTVendu':vente.prixHTVendu})
        totalTps+= vente.item.calculTps(taxes)
        totalTvq+= vente.item.calculTvq(taxes)
#    a.append(ventes_data)
    max_num = 10
    initial_vente =  []
    for indice_vente in range(max_num): 
        if indice_vente < len(ventes_data):
            a.append(10)
            item = ventes_data[indice_vente]['item']
            noVente = ventes_data[indice_vente]['noVente'] 
            prixHTVendu = ventes_data[indice_vente]['prixHTVendu'] 
        else : 
            item = None
            noVente = trans.noTrans+'0'+str(indice_vente)
            prixHTVendu = 0 
        initial_vente.append({'item' : item, 'noVente':noVente, 'prixHTVendu':prixHTVendu})  
        totalPrixHT+= prixHTVendu
    a.append(initial_vente)      

    totalPrixTC = totalPrixHT + totalTvq + totalTps
    
    VenteFormSet = modelformset_factory(Vente,form=VenteForm, extra=max_num, max_num=max_num, can_delete=False)   
    envoi = False
    if request.method == 'POST':
        a.append(1)
        transac_form = TransactionForm(request.POST, prefix='transaction', initial=initial_trans)
        #MANAGE INPUT DATA
        i=0
        if "annuler" in request.POST:
            existe_trans = Transaction.objects.filter(noTrans=trans.noTrans)
            for existe in existe_trans:
                existe.delete()
            global noTrans
            noTrans =Transaction.objects.all().last().noTrans
#            return render({}, 'ventes/modifier_transaction.html', locals())
            return redirect(modifier_transaction)
            
        if transac_form.is_valid():
            a.append(7)
            transac = transac_form.save(commit=False)
            transac.noTrans = trans.noTrans
            transac.client = transac_form.cleaned_data['client']
            transac.moyenPaiement = transac_form.cleaned_data['moyenPaiement']
            transac.vendeur = transac_form.cleaned_data['vendeur']
                
            existe_trans = Transaction.objects.filter(noTrans=trans.noTrans)
            for existe in existe_trans:
                transac.payee=existe.payee
                existe.delete()
                        
            if "payer" in request.POST:
                transac.payee=True
        
            transac.save() 
            vente_formset = VenteFormSet(request.POST, queryset=Vente.objects.none(), initial=initial_vente, prefix='vente')  
                       
#            if vente_formset.is_valid(): 
            for vente_form in vente_formset:
                if vente_form.is_valid():
                    a.append(6)                                  
                    noItem = request.POST[vente_formset.prefix+'-'+str(i)+'-item']
                    noVente = request.POST[vente_formset.prefix+'-'+str(i)+'-noVente']
                    prixHT = request.POST[vente_formset.prefix+'-'+str(i)+'-prixHTVendu']
                    i+=1
                    if noItem:
                        a.append(5)
                        vente = vente_form.save(commit=False)
                        vente.noVente = noVente
                        existe_vente = Vente.objects.filter(noVente=noVente)
                        if existe_vente:
                            existe_vente[0].delete()     
                        vente.item = Item.objects.get(noRef=noItem)
                        vente.prixHTVendu = vente.item.prixHT
                        vente.noTrans = transac
                        vente.save()
                else:
                    a.append(4)

            return redirect(faire_vente)
    else:
        a.append(3)
        a.append(request)
        transac_form = TransactionForm(prefix='transaction', initial=initial_trans)
        vente_formset = VenteFormSet(queryset=Vente.objects.none(), initial=initial_vente, prefix='vente') 

#Eleve.objects.aggregate(Avg('moyenne'))
    return render(request, 'ventes/faireVente.html', locals())
    
def modifier_transaction(request):
    global noTrans, b
    if request.POST and 'transaction' in request.POST:
        form = ChoixTransForm(request.POST)
        noTrans = request.POST['transaction']
        b = 1
        return redirect(faire_vente)
    else:
        form = ChoixTransForm()
        b = 2
    return render(request, 'ventes/transactions.html', {'form':form, 'b':b})
    
         
    
'''
    if vente_formset.is_valid():
        nvl_vente = []
        for vente_form in vente_formset:
            item = vente_form.cleaned_data.get('item')
            if item:
                noVentes = []
                for vente in vente_formet:
                    noVentes.append(vente.noVente)
                if not noVentes:
                    dernierNoVente = trans.noTrans + '000'
                else:
                    dernierNoVente = max(noVentes)
                nbVente = eval(dernierNoVente[-2:])
                if nbVente<9:
                    noVente = dernierNoVente[:-1] + str(nbVente+1)
                else : 
                    noVente = dernierNoVente[:-2] + str(nbVente+1)
                nvl_vente.append(Vente(noVente=noVente, noTrans=trans,item=item))
                try:
                    with transaction.atomic():
                        #Replace the old with the new
                        Vente.objects.filter(noTrans=noTrans).delete()
                        Vente.objects.bulk_create(new_links)
                        messages.success(my_post_dict, 'You have updated your profile.')

                except IntegrityError: #If the transaction failed
                    messages.error(my_post_dict, 'There was an error saving your profile.')
                    return redirect(reverse('profile-settings'))'''
#    return render(request, 'app_bdd/faireVente.html', {'ventes_t': ventes_trans,'trans':trans,'formset': vente_formset})

'''
    request_post_copy = request.POST.copy()
    request_post_copy.update({
        'form-TOTAL_FORMS': 1,
        'form-INITIAL_FORMS': 0,
        'form-MAX_NUM_FORMS': 5,
    })
    
    
    

#    VenteFormSet = inlineformset_factory(Transaction,Vente, fields=('item',), extra=3)
    data = {
    'form-TOTAL_FORMS': '2',
    'form-INITIAL_FORMS': '0',
    'form-MAX_NUM_FORMS': ''}
    if request.method=='POST':
#        trans_form = TransactionForm(data.update(request.POST), instance=trans, prefix='trans')
        formset = VenteFormSet(request.POST, instance=trans, prefix='vente')
    if trans_form.is_valid() and formset.is_valid():
        r = trans_form.save(commit=False)
        formset.save()
        r.save()
        
    return render(request, 'app_bdd/faireVente.html', {'trans_form':trans_form,'formset': formset})'''

'''    data = {
    'form-TOTAL_FORMS': '5',
    'form-INITIAL_FORMS': '0',
    'form-MAX_NUM_FORMS': ''}
    VenteFormSet = modelformset_factory(Vente, fields=('item',))
    formset = VenteFormSet(request.POST or None, request.FILES)
    if formset.is_valid():
        ventes = formset.save(commit=False)
        for form in ventes:
            vente = form.save(commit=False)
            item = form.cleaned_data['item']
            prixHT = item.prixHT
            taxes = Taxes.objects.order_by('date')[0]
            prixTC = item.calculPrixTTC(taxes)
            dernierNoTrans = Transaction.objects.order_by('dateTrans')[0].noTrans 
            noTrans = str(dernierNoTrans)
            nbVentesParTrans = len(Vente.objects.filter(noVente__contains=noTrans))
            if nbVentesParTrans<9:
                noVente = noTrans + '0' +str(nbVentesParTrans+1)
            else:
                noVente = noTrans + nbVentesParTrans
            vente.noVente = noVente
            vente.noTrans = Transaction.objects.get(noTrans=noTrans)
            vente.save()
        formset.save()'''

'''def ajoutMembre(request):
    form = AjoutMembre(request.POST or None)
    if form.is_valid():
        nom =  form.cleaned_data['nom']
        prenom =  form.cleaned_data['prenom']
        courriel =  form.cleaned_data['courriel']
        cp =  form.cleaned_data['cp']
        telephone =  form.cleaned_data['telephone']
        dateAdh = form.cleaned_data['dateAdh']
        idMembre = '''
        
     

