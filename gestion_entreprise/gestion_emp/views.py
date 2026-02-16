from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employe
from .forms import EmployeForm

# Vue pour la liste des employés
def liste_employes(request):
    employes = Employe.objects.all()
    context = {
        'employes': employes,
        'total_employes': employes.count(),
        'employes_actifs': employes.filter(statut='actif').count(),
    }
    return render(request, 'gestion_emp/liste_employes.html', context)

# Vue pour les détails d'un employé
def detail_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    context = {
        'employe': employe,
    }
    return render(request, 'gestion_emp/detail_employe.html', context)

# Vue pour ajouter un employé
def ajouter_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employé ajouté avec succès!')
            return redirect('liste_employes')
    else:
        form = EmployeForm()
    
    context = {
        'form': form,
        'titre': 'Ajouter un employé'
    }
    return render(request, 'gestion_emp/form_employe.html', context)

# Vue pour modifier un employé
def modifier_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employé modifié avec succès!')
            return redirect('detail_employe', pk=employe.pk)
    else:
        form = EmployeForm(instance=employe)
    
    context = {
        'form': form,
        'titre': 'Modifier un employé',
        'employe': employe
    }
    return render(request, 'gestion_emp/form_employe.html', context)

# Vue pour supprimer un employé
def supprimer_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        employe.delete()
        messages.success(request, 'Employé supprimé avec succès!')
        return redirect('liste_employes')
    
    context = {
        'employe': employe
    }
    return render(request, 'gestion_emp/confirmer_suppression.html', context)