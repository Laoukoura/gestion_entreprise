from django.contrib import admin
from .models import Employe

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'poste', 'departement', 'statut', 'date_embauche')
    list_filter = ('statut', 'poste', 'departement', 'genre')
    search_fields = ('matricule', 'nom', 'prenom', 'email')
    ordering = ('-date_embauche',)
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('matricule', 'nom', 'prenom', 'genre', 'date_naissance', 'lieu_naissance')
        }),
        ('Contacts', {
            'fields': ('telephone', 'email', 'adresse')
        }),
        ('Informations professionnelles', {
            'fields': ('poste', 'departement', 'date_embauche', 'salaire_base', 'statut')
        }),
    )