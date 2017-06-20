# Create your views here.
from datetime import date, datetime
from django.utils import timezone
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import render, redirect, render_to_response
from django.forms import modelformset_factory,inlineformset_factory
from django.db import IntegrityError, transaction
from .models import *
from .forms import *

def genererNoTrans():
    '''
    genere un numero de transaction en fonction de la date
    '''
    
    dateTrans = date.today()
    str_date = dateTrans.strftime("%Y%m%d")
    #si aucune transaction du tout, en crée une avec la date d aujourd hui suivi de '000'
    trans_ajd = Transaction.objects.filter(noTrans__contains=str_date) 
    if len(trans_ajd)==0:
        str_date = date.today().strftime("%Y%m%d")
        noTrans = str_date+'000'
    #sinon, prend le dernier numero et lui ajoute un
    else:
        noTrans = str(eval(trans_ajd.latest('noTrans').noTrans)+1)
    return noTrans

generation_noTans = genererNoTrans()
noTrans = generation_noTans
#prend la taxe en vigueur
taxes = Taxes.objects.order_by('date').last()

def ajouter_transaction(request):
    '''
    crée un nouveau numero de transaction 
    '''
    global noTrans, taxes
    noTrans = genererNoTrans()
    taxes = Taxes.objects.order_by('date').last()
    if request.POST:
        return redirect(faire_vente)
    return render(request, 'ventes/transactions.html', locals())

def faire_vente(request):
    '''
    fonction qui permet d enregistrer une nouvelle transaction avec ses ventes
    '''
    
    #*************************************************************************************************************************************
    #AFFICHAGE DES DONNEES INITIALES   
    
    #-----------------------------------------------------
    ########### TRANSACTIONS #############
    global taxes
    taxes = Taxes.objects.order_by('date').last()
    #recupere le numero de trans global de views.py
    try:
        trans = Transaction.objects.get(noTrans=noTrans)
        initial_trans = {'moyenPaiement':trans.moyenPaiement, 'benevole':trans.benevole, 'commentaire':trans.commentaire}
        initial_nom= trans.client.nom
        initial_prenom = trans.client.prenom
        initial_courriel = trans.client.courriel  
        existant = True 
        
    #dans le cas ou aucune transaction ne correspond au numero généré
    except:
        trans = Transaction(noTrans=noTrans, client=Client('','',''), moyenPaiement='', benevole=Benevole.objects.all()[0], commentaire='')
        initial_trans =  {'moyenPaiement':None, 'benevole':None, 'commentaire':''}
        initial_nom = initial_prenom = initial_courriel = ''
        existant = False
        
    
    #--------------------------------------------------    
    ############ VENTES ###################
    
    ventes_trans = Vente.objects.filter(noTrans=trans)
    totalPrixHT = totalTps = totalTvq = totalPrixTC = 0
            
    #ne peut acheter que 10 items par transaction car je n ai pas reussi a gerer l affichage de plus d elements
    # en utilisant du js, on pourrait supprimer cette variable      
    max_num = 10 
    initial_vente =  []
    for indice_vente in range(max_num): 
        if indice_vente < len(ventes_trans):
            # s il existe une vente associé a cette indice dans la base de données
            content_object = ventes_trans[indice_vente].content_object
            noRef = ventes_trans[indice_vente].content_object.noRef
            noVente = ventes_trans[indice_vente].noVente
            prixHTVendu = ventes_trans[indice_vente].prixHTVendu 
            totalPrixHT += prixHTVendu
            totalTps += ventes_trans[indice_vente].get_tps(taxes)
            totalTvq += ventes_trans[indice_vente].get_tvq(taxes)
            totalPrixTC += ventes_trans[indice_vente].get_prixTCVendu(taxes)         
        else : 
            noRef = None
            noVente = trans.noTrans+'0'+str(indice_vente)
            prixHTVendu = 0 
        initial_vente.append({'item' : noRef, 'noVente':noVente, 'prixHTVendu':prixHTVendu})  
    
    #**************************************************************************************************************
    
    VenteFormSet = modelformset_factory(Vente,form=VenteForm, extra=max_num, max_num=max_num, can_delete=False)   
    envoi = False
    if request.method == 'POST':
        transac_form = TransactionForm(request.POST, prefix='transaction', initial=initial_trans)
        if "annuler" in request.POST:
            #si le benevole effectue l action pour supprimer une transaction
            try:
                Transaction.objects.get(noTrans=trans.noTrans).delete()
            except:
                pass
            # genere un nouveau numero de transaction car l actuel est supprimé             
            global noTrans
            noTrans =genererNoTrans()
            return redirect(modifier_transaction) 
                                         
        if "nom" in request.POST and "prenom" in request.POST:
            #si le benevole a rempli les champs pour le nom et le prenom          
            client_nom = request.POST['nom']
            client_prenom = request.POST['prenom']
            try:
                #va chercher s il existe dans la base un client qui a le nom et prenom rentré dans le formulaire
                client = Client.objects.get(nom=client_nom,prenom=client_prenom)
            except:
                #si ce client n exite pas encore, alors, on le crée
                client_courriel = request.POST["courriel"]
                client = Client(nom=client_nom, prenom=client_prenom, courriel=client_courriel)
                client.save()     
            
        if transac_form.is_valid():
            transac = transac_form.save(commit=False)
            transac.noTrans = trans.noTrans
            transac.client = client
            transac.moyenPaiement = transac_form.cleaned_data['moyenPaiement']
            transac.benevole = transac_form.cleaned_data['benevole']
            existe_trans = Transaction.objects.filter(noTrans=transac.noTrans)
            if len(existe_trans)>0:
                #s il existe déjà dans la base une transaction avec le numero ici attribué
                # alors on supprime la transaction pour l ecraser avec les nouvelles données
                # on ne garde que l info si la transaction etait payee ou non
                transac.payee=existe_trans[0].payee
                existe_trans.delete()
                        
            if "payer" in request.POST:
                transac.payee=True
            transac.save() 
            
            vente_formset = VenteFormSet(request.POST, queryset=Vente.objects.none(), initial=initial_vente,prefix='vente') 
            i=0           
            for vente_form in vente_formset:
                if vente_form.is_valid():               
                    noVente = request.POST[vente_formset.prefix+'-'+str(i)+'-noVente']               
                    noItem = request.POST[vente_formset.prefix+'-'+str(i)+'-item']
                    prixHT = request.POST[vente_formset.prefix+'-'+str(i)+'-prixHTVendu']
                    if noItem:
                        #si le benevole a rentré un item dans la ligne
                        vente = vente_form.save(commit=False)
                        vente.noVente = noVente
                        try:
                            #supprime les ventes qui pourraient avoir le meme numero
                            Vente.objects.get(noVente=noVente).delete()
                        except:
                            pass
                        
                        #regarde tous les items existants a partir des classes filles    
                        for classe in Item.__subclasses__():
                            for elmt in classe.objects.all():
                                if elmt.noRef==eval(noItem):
                                    vente.content_object= elmt
                        if vente.content_object :
                            #s il a trouvé un item qui match
                            if prixHT=='0' :
                                vente.prixHTVendu = vente.content_object.prixHT
                            else:
                                vente.prixHTVendu = prixHT
                            vente.noTrans = transac
                            vente.save() 
                    i+=1
            #redirect pour supprimer tous les affichages indesirables
            return redirect(faire_vente)
    else:
        transac_form = TransactionForm(prefix='transaction', initial=initial_trans)
        vente_formset = VenteFormSet(queryset=Vente.objects.none(), initial=initial_vente, prefix='vente') 
        
    return render(request, 'ventes/faireVente.html', locals())
    
def modifier_transaction(request):
    global noTrans, taxes
    taxes = Taxes.objects.order_by('date').last()
    
    if request.POST and 'transaction' in request.POST:
        trans_form = ChoixTransForm(request.POST)
        noTrans = request.POST['transaction']
        return redirect(faire_vente)
    else:
        trans_form = ChoixTransForm()
    
    date_balance = form = ChoixDate(request.POST)
    return render(request, 'ventes/transactions.html', {'trans_form':trans_form, 'date_balance':date_balance})
    
def balance_journee(request):
    if request.POST:
        jour = timezone.datetime.strptime(request.POST['date'], '%m/%d/%Y').date()
        transac = Transaction.objects.filter(dateTrans__contains=jour, payee=True)
        total_debit = total_comptant = total_ligne = total_HT = total_TC = 0
        for t in transac:
            total_HT += t.get_totalHT()
            total_TC += t.get_totalTC()
            if t.moyenPaiement == 'DEBIT':
                total_debit += t.get_totalTC()
            elif t.moyenPaiement == 'COMPTANT':
                total_comptant += t.get_totalTC()
            elif t.moyenPaiement == 'LIGNE':
                total_ligne += t.get_totalTC()
    return render(request, 'ventes/balance.html', locals())

            

 
