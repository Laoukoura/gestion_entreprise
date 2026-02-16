from django.contrib import admin
from .models import TypeElement, ParametrePaie, BulletinPaie, ElementPaie

@admin.register(TypeElement)
class TypeElementAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'type_element', 'actif')
    list_filter = ('type_element', 'actif')
    search_fields = ('nom', 'code')

@admin.register(ParametrePaie)
class ParametrePaieAdmin(admin.ModelAdmin):
    list_display = ('date_application', 'taux_cotisation_employe', 'taux_cotisation_employeur', 'actif')
    list_filter = ('actif', 'date_application')
    fieldsets = (
        ('Cotisations sociales', {
            'fields': ('taux_cotisation_employe', 'taux_cotisation_employeur')
        }),
        ('Heures supplémentaires', {
            'fields': ('taux_heure_sup_normale', 'taux_heure_sup_nuit', 'taux_heure_sup_weekend', 'heures_travail_mensuel')
        }),
        ('Barème d\'imposition', {
            'fields': (
                ('tranche1_max', 'tranche1_taux'),
                ('tranche2_max', 'tranche2_taux'),
                ('tranche3_max', 'tranche3_taux'),
                ('tranche4_max', 'tranche4_taux'),
                'tranche5_taux',
            )
        }),
        ('Métadonnées', {
            'fields': ('date_application', 'actif')
        }),
    )

@admin.register(BulletinPaie)
class BulletinPaieAdmin(admin.ModelAdmin):
    list_display = ('employe', 'mois', 'annee', 'salaire_brut', 'salaire_net', 'paye', 'date_paiement')
    list_filter = ('paye', 'annee', 'mois')
    search_fields = ('employe__nom', 'employe__prenom', 'employe__matricule')
    
    readonly_fields = (
        'salaire_brut', 'total_primes', 'total_deductions',
        'cotisation_sociale_employe', 'cotisation_sociale_employeur',
        'salaire_imposable', 'impot_revenu', 'salaire_net',
        'montant_heures_sup_normales', 'montant_heures_sup_nuit', 'montant_heures_sup_weekend'
    )
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('employe', 'mois', 'annee')
        }),
        ('Salaire de base', {
            'fields': ('salaire_base',)
        }),
        ('Heures supplémentaires', {
            'fields': (
                ('heures_sup_normales', 'montant_heures_sup_normales'),
                ('heures_sup_nuit', 'montant_heures_sup_nuit'),
                ('heures_sup_weekend', 'montant_heures_sup_weekend'),
            )
        }),
        ('Calculs', {
            'fields': (
                'total_primes',
                'salaire_brut',
                'cotisation_sociale_employe',
                'cotisation_sociale_employeur',
                'salaire_imposable',
                'impot_revenu',
                'total_deductions',
                'salaire_net',
            )
        }),
        ('Paiement', {
            'fields': ('paye', 'date_paiement')
        }),
    )
    
@admin.register(ElementPaie)
class ElementPaieAdmin(admin.ModelAdmin):
    list_display = ('bulletin', 'type_element', 'montant', 'commentaire')
    list_filter = ('type_element__type_element', 'bulletin__annee', 'bulletin__mois')
    search_fields = ('bulletin__employe__nom', 'type_element__nom', 'commentaire')
    autocomplete_fields = ['bulletin']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Recalculer le bulletin après ajout d'un élément
        obj.bulletin.calculer_paie()