from django.db import models
from gestion_emp.models import Employe
from decimal import Decimal

class TypeElement(models.Model):
    """Types d'éléments de paie (primes, déductions)"""
    TYPE_CHOICES = [
        ('prime', 'Prime'),
        ('deduction', 'Déduction'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    type_element = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    description = models.TextField(blank=True, verbose_name="Description")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Type d'élément"
        verbose_name_plural = "Types d'éléments"
    
    def __str__(self):
        return f"{self.code} - {self.nom}"


class ParametrePaie(models.Model):
    """Paramètres généraux pour les calculs de paie"""
    
    # Cotisations sociales (en pourcentage)
    taux_cotisation_employe = models.DecimalField(
        max_digits=5, decimal_places=2, default=5.00,
        verbose_name="Taux cotisation employé (%)"
    )
    taux_cotisation_employeur = models.DecimalField(
        max_digits=5, decimal_places=2, default=16.00,
        verbose_name="Taux cotisation employeur (%)"
    )
    
    # Heures supplémentaires
    taux_heure_sup_normale = models.DecimalField(
        max_digits=5, decimal_places=2, default=125.00,
        verbose_name="Taux heure sup normale (% du taux horaire)"
    )
    taux_heure_sup_nuit = models.DecimalField(
        max_digits=5, decimal_places=2, default=150.00,
        verbose_name="Taux heure sup de nuit (% du taux horaire)"
    )
    taux_heure_sup_weekend = models.DecimalField(
        max_digits=5, decimal_places=2, default=175.00,
        verbose_name="Taux heure sup week-end (% du taux horaire)"
    )
    
    # Barème d'imposition (impôt sur le revenu)
    tranche1_max = models.DecimalField(max_digits=12, decimal_places=2, default=30000, verbose_name="Tranche 1 max")
    tranche1_taux = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Taux tranche 1 (%)")
    
    tranche2_max = models.DecimalField(max_digits=12, decimal_places=2, default=50000, verbose_name="Tranche 2 max")
    tranche2_taux = models.DecimalField(max_digits=5, decimal_places=2, default=10, verbose_name="Taux tranche 2 (%)")
    
    tranche3_max = models.DecimalField(max_digits=12, decimal_places=2, default=80000, verbose_name="Tranche 3 max")
    tranche3_taux = models.DecimalField(max_digits=5, decimal_places=2, default=15, verbose_name="Taux tranche 3 (%)")
    
    tranche4_max = models.DecimalField(max_digits=12, decimal_places=2, default=120000, verbose_name="Tranche 4 max")
    tranche4_taux = models.DecimalField(max_digits=5, decimal_places=2, default=20, verbose_name="Taux tranche 4 (%)")
    
    tranche5_taux = models.DecimalField(max_digits=5, decimal_places=2, default=25, verbose_name="Taux tranche 5 (%)")
    
    # Nombre d'heures de travail standard
    heures_travail_mensuel = models.IntegerField(default=173, verbose_name="Heures de travail mensuel")
    
    actif = models.BooleanField(default=True, verbose_name="Paramètre actif")
    date_application = models.DateField(verbose_name="Date d'application")
    
    class Meta:
        verbose_name = "Paramètre de paie"
        verbose_name_plural = "Paramètres de paie"
        ordering = ['-date_application']
    
    def __str__(self):
        return f"Paramètres du {self.date_application}"
    
    def calculer_impot(self, salaire_imposable):
        """Calcule l'impôt selon le barème progressif"""
        impot = Decimal('0.00')
        reste = salaire_imposable
        
        # Tranche 1
        if reste > 0:
            montant_tranche = min(reste, self.tranche1_max)
            impot += montant_tranche * (self.tranche1_taux / 100)
            reste -= montant_tranche
        
        # Tranche 2
        if reste > 0:
            montant_tranche = min(reste, self.tranche2_max - self.tranche1_max)
            impot += montant_tranche * (self.tranche2_taux / 100)
            reste -= montant_tranche
        
        # Tranche 3
        if reste > 0:
            montant_tranche = min(reste, self.tranche3_max - self.tranche2_max)
            impot += montant_tranche * (self.tranche3_taux / 100)
            reste -= montant_tranche
        
        # Tranche 4
        if reste > 0:
            montant_tranche = min(reste, self.tranche4_max - self.tranche3_max)
            impot += montant_tranche * (self.tranche4_taux / 100)
            reste -= montant_tranche
        
        # Tranche 5
        if reste > 0:
            impot += reste * (self.tranche5_taux / 100)
        
        return impot.quantize(Decimal('0.01'))


class BulletinPaie(models.Model):
    """Bulletin de paie mensuel"""
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='bulletins')
    mois = models.IntegerField(verbose_name="Mois")
    annee = models.IntegerField(verbose_name="Année")
    
    # Salaires
    salaire_base = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Salaire de base")
    
    # Heures supplémentaires
    heures_sup_normales = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Heures sup normales")
    montant_heures_sup_normales = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Montant heures sup normales")
    
    heures_sup_nuit = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Heures sup de nuit")
    montant_heures_sup_nuit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Montant heures sup de nuit")
    
    heures_sup_weekend = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Heures sup week-end")
    montant_heures_sup_weekend = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Montant heures sup week-end")
    
    # Totaux primes et déductions
    total_primes = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total primes")
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total déductions")
    
    # Calculs
    salaire_brut = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Salaire brut")
    cotisation_sociale_employe = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Cotisation sociale employé")
    cotisation_sociale_employeur = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Cotisation sociale employeur")
    salaire_imposable = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Salaire imposable")
    impot_revenu = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Impôt sur le revenu")
    salaire_net = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Salaire net")
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_paiement = models.DateField(null=True, blank=True, verbose_name="Date de paiement")
    paye = models.BooleanField(default=False, verbose_name="Payé")
    
    parametres = models.ForeignKey(ParametrePaie, on_delete=models.PROTECT, verbose_name="Paramètres utilisés", null=True, blank=True)
    
    class Meta:
        verbose_name = "Bulletin de paie"
        verbose_name_plural = "Bulletins de paie"
        unique_together = ['employe', 'mois', 'annee']
        ordering = ['-annee', '-mois']
    
    def __str__(self):
        return f"Paie {self.employe.matricule} - {self.mois}/{self.annee}"
    
    def calculer_paie(self):
        """Calcule tous les éléments du bulletin de paie"""
        # Récupérer les paramètres actifs
        if not self.parametres:
            self.parametres = ParametrePaie.objects.filter(actif=True).first()
            if not self.parametres:
                raise ValueError("Aucun paramètres de paie actif trouvé. Veuillez en créer un.")
        
        # Salaire de base
        self.salaire_base = self.employe.salaire_base
        
        # Calcul du taux horaire
        taux_horaire = self.salaire_base / self.parametres.heures_travail_mensuel
        
        # Calcul des heures supplémentaires
        self.montant_heures_sup_normales = (
            self.heures_sup_normales * taux_horaire * 
            (self.parametres.taux_heure_sup_normale / 100)
        )
        self.montant_heures_sup_nuit = (
            self.heures_sup_nuit * taux_horaire * 
            (self.parametres.taux_heure_sup_nuit / 100)
        )
        self.montant_heures_sup_weekend = (
            self.heures_sup_weekend * taux_horaire * 
            (self.parametres.taux_heure_sup_weekend / 100)
        )
        
        # Calcul du total des primes (depuis ElementPaie)
        primes = self.elements.filter(type_element__type_element='prime')
        self.total_primes = sum(e.montant for e in primes) + \
                           self.montant_heures_sup_normales + \
                           self.montant_heures_sup_nuit + \
                           self.montant_heures_sup_weekend
        
        # Salaire brut
        self.salaire_brut = self.salaire_base + self.total_primes
        
        # Cotisations sociales
        self.cotisation_sociale_employe = (
            self.salaire_brut * (self.parametres.taux_cotisation_employe / 100)
        )
        self.cotisation_sociale_employeur = (
            self.salaire_brut * (self.parametres.taux_cotisation_employeur / 100)
        )
        
        # Salaire imposable
        self.salaire_imposable = self.salaire_brut - self.cotisation_sociale_employe
        
        # Impôt sur le revenu
        self.impot_revenu = self.parametres.calculer_impot(self.salaire_imposable)
        
        # Calcul du total des déductions (depuis ElementPaie)
        deductions = self.elements.filter(type_element__type_element='deduction')
        self.total_deductions = sum(e.montant for e in deductions) + \
                               self.cotisation_sociale_employe + \
                               self.impot_revenu
        
        # Salaire net
        self.salaire_net = self.salaire_brut - self.total_deductions
        
        # Arrondir tous les montants
        self.salaire_brut = self.salaire_brut.quantize(Decimal('0.01'))
        self.cotisation_sociale_employe = self.cotisation_sociale_employe.quantize(Decimal('0.01'))
        self.cotisation_sociale_employeur = self.cotisation_sociale_employeur.quantize(Decimal('0.01'))
        self.salaire_imposable = self.salaire_imposable.quantize(Decimal('0.01'))
        self.impot_revenu = self.impot_revenu.quantize(Decimal('0.01'))
        self.salaire_net = self.salaire_net.quantize(Decimal('0.01'))
        
        self.save()


class ElementPaie(models.Model):
    """Élément de paie individuel (prime ou déduction)"""
    bulletin = models.ForeignKey(BulletinPaie, on_delete=models.CASCADE, related_name='elements')
    type_element = models.ForeignKey(TypeElement, on_delete=models.PROTECT)
    montant = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant")
    commentaire = models.CharField(max_length=200, blank=True, verbose_name="Commentaire")
    
    class Meta:
        verbose_name = "Élément de paie"
        verbose_name_plural = "Éléments de paie"
    
    def __str__(self):
        return f"{self.type_element.nom} - {self.montant}"