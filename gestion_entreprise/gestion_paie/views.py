from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Q
from decimal import Decimal
from .models import BulletinPaie, ElementPaie, TypeElement, ParametrePaie
from gestion_emp.models import Employe
from .forms import BulletinPaieForm, ElementPaieForm, GenerationMasseBulletinsForm, RechercherBulletinForm

# Vue tableau de bord
def tableau_bord_paie(request):
    """Tableau de bord avec statistiques"""
    bulletins = BulletinPaie.objects.all()
    
    # Statistiques globales
    total_masse_salariale = bulletins.aggregate(total=Sum('salaire_net'))['total'] or 0
    total_bulletins = bulletins.count()
    bulletins_payes = bulletins.filter(paye=True).count()
    bulletins_en_attente = bulletins.filter(paye=False).count()
    
    # Derniers bulletins créés
    derniers_bulletins = bulletins.order_by('-date_creation')[:5]
    
    context = {
        'total_masse_salariale': total_masse_salariale,
        'total_bulletins': total_bulletins,
        'bulletins_payes': bulletins_payes,
        'bulletins_en_attente': bulletins_en_attente,
        'derniers_bulletins': derniers_bulletins,
    }
    return render(request, 'gestion_paie/tableau_bord.html', context)

# Vue liste des bulletins
def liste_bulletins(request):
    """Liste de tous les bulletins avec recherche"""
    bulletins = BulletinPaie.objects.all().select_related('employe')
    form = RechercherBulletinForm(request.GET)
    
    # Filtrage
    if form.is_valid():
        if form.cleaned_data.get('employe'):
            bulletins = bulletins.filter(employe=form.cleaned_data['employe'])
        if form.cleaned_data.get('mois'):
            bulletins = bulletins.filter(mois=form.cleaned_data['mois'])
        if form.cleaned_data.get('annee'):
            bulletins = bulletins.filter(annee=form.cleaned_data['annee'])
        if form.cleaned_data.get('paye') == 'oui':
            bulletins = bulletins.filter(paye=True)
        elif form.cleaned_data.get('paye') == 'non':
            bulletins = bulletins.filter(paye=False)
    
    context = {
        'bulletins': bulletins,
        'form': form,
        'total_bulletins': bulletins.count(),
    }
    return render(request, 'gestion_paie/liste_bulletins.html', context)

# Vue détails d'un bulletin
def detail_bulletin(request, pk):
    """Affiche les détails d'un bulletin de paie"""
    bulletin = get_object_or_404(BulletinPaie, pk=pk)
    elements_primes = bulletin.elements.filter(type_element__type_element='prime')
    elements_deductions = bulletin.elements.filter(type_element__type_element='deduction')
    
    context = {
        'bulletin': bulletin,
        'elements_primes': elements_primes,
        'elements_deductions': elements_deductions,
    }
    return render(request, 'gestion_paie/detail_bulletin.html', context)

# Vue créer un bulletin
def creer_bulletin(request):
    """Créer un nouveau bulletin de paie"""
    if request.method == 'POST':
        form = BulletinPaieForm(request.POST)
        if form.is_valid():
            bulletin = form.save(commit=False)
            bulletin.salaire_base = bulletin.employe.salaire_base
            bulletin.save()
            messages.success(request, 'Bulletin de paie créé avec succès!')
            return redirect('detail_bulletin', pk=bulletin.pk)
    else:
        form = BulletinPaieForm()
    
    context = {
        'form': form,
        'titre': 'Créer un bulletin de paie'
    }
    return render(request, 'gestion_paie/form_bulletin.html', context)

# Vue modifier un bulletin
def modifier_bulletin(request, pk):
    """Modifier un bulletin existant"""
    bulletin = get_object_or_404(BulletinPaie, pk=pk)
    
    if request.method == 'POST':
        form = BulletinPaieForm(request.POST, instance=bulletin)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bulletin modifié avec succès!')
            return redirect('detail_bulletin', pk=bulletin.pk)
    else:
        form = BulletinPaieForm(instance=bulletin)
    
    context = {
        'form': form,
        'titre': 'Modifier le bulletin',
        'bulletin': bulletin
    }
    return render(request, 'gestion_paie/form_bulletin.html', context)

# Vue supprimer un bulletin
def supprimer_bulletin(request, pk):
    """Supprimer un bulletin"""
    bulletin = get_object_or_404(BulletinPaie, pk=pk)
    
    if request.method == 'POST':
        bulletin.delete()
        messages.success(request, 'Bulletin supprimé avec succès!')
        return redirect('liste_bulletins')
    
    context = {
        'bulletin': bulletin
    }
    return render(request, 'gestion_paie/confirmer_suppression_bulletin.html', context)

# Vue ajouter un élément de paie
def ajouter_element(request, bulletin_pk):
    """Ajouter un élément (prime/déduction) à un bulletin"""
    bulletin = get_object_or_404(BulletinPaie, pk=bulletin_pk)
    
    if request.method == 'POST':
        form = ElementPaieForm(request.POST)
        if form.is_valid():
            element = form.save(commit=False)
            element.bulletin = bulletin
            element.save()
            bulletin.calculer_paie()
            messages.success(request, f'{element.type_element.nom} ajouté avec succès!')
            return redirect('detail_bulletin', pk=bulletin.pk)
    else:
        form = ElementPaieForm()
    
    context = {
        'form': form,
        'bulletin': bulletin,
        'titre': f'Ajouter un élément à {bulletin}'
    }
    return render(request, 'gestion_paie/form_element.html', context)

# Vue supprimer un élément
def supprimer_element(request, pk):
    """Supprimer un élément de paie"""
    element = get_object_or_404(ElementPaie, pk=pk)
    bulletin = element.bulletin
    
    if request.method == 'POST':
        element.delete()
        bulletin.calculer_paie()
        messages.success(request, 'Élément supprimé avec succès!')
        return redirect('detail_bulletin', pk=bulletin.pk)
    
    context = {
        'element': element
    }
    return render(request, 'gestion_paie/confirmer_suppression_element.html', context)

# Vue marquer comme payé
def marquer_paye(request, pk):
    """Marquer un bulletin comme payé"""
    bulletin = get_object_or_404(BulletinPaie, pk=pk)
    
    if request.method == 'POST':
        from datetime import date
        bulletin.paye = True
        bulletin.date_paiement = date.today()
        bulletin.save()
        messages.success(request, 'Bulletin marqué comme payé!')
        return redirect('detail_bulletin', pk=bulletin.pk)
    
    context = {
        'bulletin': bulletin
    }
    return render(request, 'gestion_paie/confirmer_paiement.html', context)

# Vue génération en masse
def generer_bulletins_masse(request):
    """Générer des bulletins pour plusieurs employés"""
    if request.method == 'POST':
        form = GenerationMasseBulletinsForm(request.POST)
        if form.is_valid():
            mois = int(form.cleaned_data['mois'])
            annee = int(form.cleaned_data['annee'])
            departement = form.cleaned_data.get('departement')
            statut = form.cleaned_data.get('statut')
            
            # Filtrer les employés
            employes = Employe.objects.all()
            if departement:
                employes = employes.filter(departement__icontains=departement)
            if statut:
                employes = employes.filter(statut=statut)
            
            bulletins_crees = 0
            bulletins_existants = 0
            
            for employe in employes:
                # Vérifier si le bulletin existe déjà
                if not BulletinPaie.objects.filter(employe=employe, mois=mois, annee=annee).exists():
                    bulletin = BulletinPaie.objects.create(
                        employe=employe,
                        mois=mois,
                        annee=annee,
                        salaire_base=employe.salaire_base
                    )
                    bulletins_crees += 1
                else:
                    bulletins_existants += 1
            
            messages.success(request, f'{bulletins_crees} bulletin(s) créé(s). {bulletins_existants} existaient déjà.')
            return redirect('liste_bulletins')
    else:
        from datetime import date
        form = GenerationMasseBulletinsForm(initial={
            'mois': date.today().month,
            'annee': date.today().year
        })
    
    context = {
        'form': form,
        'titre': 'Générer des bulletins en masse'
    }
    return render(request, 'gestion_paie/generer_masse.html', context)

# Vue historique d'un employé
def historique_employe(request, employe_pk):
    """Affiche l'historique des paies d'un employé"""
    employe = get_object_or_404(Employe, pk=employe_pk)
    bulletins = BulletinPaie.objects.filter(employe=employe).order_by('-annee', '-mois')
    
    # Statistiques
    total_verse = bulletins.aggregate(total=Sum('salaire_net'))['total'] or 0
    
    context = {
        'employe': employe,
        'bulletins': bulletins,
        'total_verse': total_verse,
    }
    return render(request, 'gestion_paie/historique_employe.html', context)