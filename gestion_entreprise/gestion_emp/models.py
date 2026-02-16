from django.db import models
from django.core.validators import RegexValidator

class Employe(models.Model):
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('conge', 'En congé'),
        ('suspendu', 'Suspendu'),
        ('demission', 'Démission'),
    ]
    
    POSTE_CHOICES = [
        ('directeur', 'Directeur'),
        ('manager', 'Manager'),
        ('chef_equipe', 'Chef d\'équipe'),
        ('employe', 'Employé'),
        ('stagiaire', 'Stagiaire'),
    ]
    
    # Informations personnelles
    matricule = models.CharField(max_length=20, unique=True, verbose_name="Matricule")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, verbose_name="Genre")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=100, verbose_name="Lieu de naissance")
    
    # Contacts
    telephone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="Numéro de téléphone invalide")
    telephone = models.CharField(validators=[telephone_regex], max_length=17, verbose_name="Téléphone")
    email = models.EmailField(unique=True, verbose_name="Email")
    adresse = models.TextField(verbose_name="Adresse")
    
    # Informations professionnelles
    poste = models.CharField(max_length=50, choices=POSTE_CHOICES, verbose_name="Poste")
    departement = models.CharField(max_length=100, verbose_name="Département")
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salaire de base")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif', verbose_name="Statut")
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"
        ordering = ['-date_embauche']
    
    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"
    
    def get_nom_complet(self):
        return f"{self.prenom} {self.nom}"
    
    def anciennete(self):
        from datetime import date
        today = date.today()
        delta = today - self.date_embauche
        return delta.days // 365