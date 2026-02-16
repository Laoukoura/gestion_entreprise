from django import forms
from .models import BulletinPaie, ElementPaie, TypeElement
from gestion_emp.models import Employe

class BulletinPaieForm(forms.ModelForm):
    class Meta:
        model = BulletinPaie
        fields = ['employe', 'mois', 'annee', 'heures_sup_normales', 'heures_sup_nuit', 'heures_sup_weekend']
        widgets = {
            'employe': forms.Select(attrs={'class': 'form-control'}),
            'mois': forms.Select(choices=[(i, i) for i in range(1, 13)], attrs={'class': 'form-control'}),
            'annee': forms.NumberInput(attrs={'class': 'form-control', 'min': '2020', 'max': '2050'}),
            'heures_sup_normales': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'heures_sup_nuit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'heures_sup_weekend': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
        labels = {
            'employe': 'Employé',
            'mois': 'Mois',
            'annee': 'Année',
            'heures_sup_normales': 'Heures supplémentaires normales',
            'heures_sup_nuit': 'Heures supplémentaires de nuit',
            'heures_sup_weekend': 'Heures supplémentaires week-end',
        }

class ElementPaieForm(forms.ModelForm):
    class Meta:
        model = ElementPaie
        fields = ['type_element', 'montant', 'commentaire']
        widgets = {
            'type_element': forms.Select(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'commentaire': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GenerationMasseBulletinsForm(forms.Form):
    """Formulaire pour générer des bulletins en masse"""
    mois = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 13)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Mois'
    )
    annee = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '2020', 'max': '2050'}),
        label='Année'
    )
    departement = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Laisser vide pour tous'}),
        label='Département (optionnel)'
    )
    statut = forms.ChoiceField(
        choices=[('', 'Tous'), ('actif', 'Actifs uniquement')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Statut des employés'
    )

class RechercherBulletinForm(forms.Form):
    """Formulaire de recherche de bulletins"""
    employe = forms.ModelChoiceField(
        queryset=Employe.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Employé'
    )
    mois = forms.ChoiceField(
        choices=[('', 'Tous')] + [(i, i) for i in range(1, 13)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Mois'
    )
    annee = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Année'
    )
    paye = forms.ChoiceField(
        choices=[('', 'Tous'), ('oui', 'Payés'), ('non', 'Non payés')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Statut de paiement'
    )